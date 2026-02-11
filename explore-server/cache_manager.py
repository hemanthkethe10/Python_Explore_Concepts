#!/usr/bin/env python3
"""
Cache Manager for Explore Server
Provides Redis-based caching with fallback to in-memory cache
"""

import json
import hashlib
import asyncio
from typing import Any, Optional, Dict, Union
from datetime import datetime, timedelta
from functools import wraps
import logging

# Try to import redis, fall back gracefully if not available
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

logger = logging.getLogger(__name__)

class CacheManager:
    """
    Unified cache manager supporting both Redis and in-memory caching
    """
    
    def __init__(self, redis_url: Optional[str] = None, default_ttl: int = 300):
        """
        Initialize cache manager
        
        Args:
            redis_url: Redis connection URL (None for in-memory only)
            default_ttl: Default TTL in seconds
        """
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.redis_client = None
        self.memory_cache: Dict[str, Dict] = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "errors": 0
        }
        
    async def initialize(self):
        """Initialize Redis connection if URL provided and Redis is available"""
        if self.redis_url and REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                # Test connection
                await self.redis_client.ping()
                logger.info("Redis cache initialized successfully")
            except Exception as e:
                logger.warning(f"Redis connection failed, using memory cache: {e}")
                self.redis_client = None
        else:
            if not REDIS_AVAILABLE:
                logger.info("Redis not available, using in-memory cache only")
            else:
                logger.info("Using in-memory cache only")
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.aclose()
    
    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key with prefix"""
        return f"explore_server:{prefix}:{identifier}"
    
    def _hash_data(self, data: Any) -> str:
        """Generate hash for complex data structures"""
        if isinstance(data, dict):
            # Sort dict for consistent hashing
            sorted_data = json.dumps(data, sort_keys=True)
        else:
            sorted_data = str(data)
        return hashlib.md5(sorted_data.encode()).hexdigest()[:16]
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache (Redis first, then memory)
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        try:
            # Try Redis first
            if self.redis_client:
                try:
                    value = await self.redis_client.get(key)
                    if value is not None:
                        self.cache_stats["hits"] += 1
                        return json.loads(value)
                except Exception as e:
                    logger.error(f"Redis get error: {e}")
                    self.cache_stats["errors"] += 1
            
            # Fallback to memory cache
            if key in self.memory_cache:
                cache_entry = self.memory_cache[key]
                # Check expiration
                if cache_entry["expires_at"] > datetime.now():
                    self.cache_stats["hits"] += 1
                    return cache_entry["value"]
                else:
                    # Remove expired entry
                    del self.memory_cache[key]
            
            self.cache_stats["misses"] += 1
            return None
            
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            self.cache_stats["errors"] += 1
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default if None)
            
        Returns:
            True if successful, False otherwise
        """
        if ttl is None:
            ttl = self.default_ttl
            
        try:
            json_value = json.dumps(value, default=str)
            
            # Try Redis first
            if self.redis_client:
                try:
                    await self.redis_client.setex(key, ttl, json_value)
                    self.cache_stats["sets"] += 1
                    return True
                except Exception as e:
                    logger.error(f"Redis set error: {e}")
                    self.cache_stats["errors"] += 1
            
            # Fallback to memory cache
            expires_at = datetime.now() + timedelta(seconds=ttl)
            self.memory_cache[key] = {
                "value": value,
                "expires_at": expires_at
            }
            self.cache_stats["sets"] += 1
            return True
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            self.cache_stats["errors"] += 1
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete key from cache
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            deleted = False
            
            # Delete from Redis
            if self.redis_client:
                try:
                    result = await self.redis_client.delete(key)
                    deleted = result > 0
                except Exception as e:
                    logger.error(f"Redis delete error: {e}")
                    self.cache_stats["errors"] += 1
            
            # Delete from memory cache
            if key in self.memory_cache:
                del self.memory_cache[key]
                deleted = True
            
            if deleted:
                self.cache_stats["deletes"] += 1
            
            return deleted
            
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            self.cache_stats["errors"] += 1
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """
        Delete keys matching pattern
        
        Args:
            pattern: Pattern to match (e.g., "users:*")
            
        Returns:
            Number of keys deleted
        """
        deleted_count = 0
        
        try:
            # Delete from Redis
            if self.redis_client:
                try:
                    keys = await self.redis_client.keys(pattern)
                    if keys:
                        deleted_count += await self.redis_client.delete(*keys)
                except Exception as e:
                    logger.error(f"Redis pattern delete error: {e}")
                    self.cache_stats["errors"] += 1
            
            # Delete from memory cache
            keys_to_delete = [key for key in self.memory_cache.keys() if self._match_pattern(key, pattern)]
            for key in keys_to_delete:
                del self.memory_cache[key]
                deleted_count += 1
            
            self.cache_stats["deletes"] += deleted_count
            return deleted_count
            
        except Exception as e:
            logger.error(f"Cache pattern delete error: {e}")
            self.cache_stats["errors"] += 1
            return 0
    
    def _match_pattern(self, key: str, pattern: str) -> bool:
        """Simple pattern matching for memory cache"""
        if pattern.endswith("*"):
            return key.startswith(pattern[:-1])
        return key == pattern
    
    async def clear_all(self) -> bool:
        """Clear all cache entries"""
        try:
            # Clear Redis
            if self.redis_client:
                try:
                    await self.redis_client.flushdb()
                except Exception as e:
                    logger.error(f"Redis clear error: {e}")
                    self.cache_stats["errors"] += 1
            
            # Clear memory cache
            self.memory_cache.clear()
            
            # Reset stats except errors
            self.cache_stats.update({
                "hits": 0,
                "misses": 0,
                "sets": 0,
                "deletes": 0
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            self.cache_stats["errors"] += 1
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            **self.cache_stats,
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2),
            "memory_cache_size": len(self.memory_cache),
            "backend": "redis" if self.redis_client else "memory",
            "default_ttl": self.default_ttl,
            "redis_available": REDIS_AVAILABLE
        }
    
    def cleanup_expired(self):
        """Clean up expired entries from memory cache"""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.memory_cache.items()
            if entry["expires_at"] <= now
        ]
        for key in expired_keys:
            del self.memory_cache[key]
        
        return len(expired_keys)


# Cache decorators
def cache_result(
    cache_manager: CacheManager,
    key_prefix: str,
    ttl: Optional[int] = None,
    key_generator: Optional[callable] = None
):
    """
    Decorator to cache function results
    
    Args:
        cache_manager: CacheManager instance
        key_prefix: Prefix for cache keys
        ttl: Time to live in seconds
        key_generator: Custom function to generate cache key from args
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_generator:
                cache_key = cache_manager._generate_key(key_prefix, key_generator(*args, **kwargs))
            else:
                # Default key generation from function args
                key_data = {"args": args, "kwargs": kwargs}
                key_hash = cache_manager._hash_data(key_data)
                cache_key = cache_manager._generate_key(key_prefix, key_hash)
            
            # Try to get from cache
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator


def invalidate_cache_pattern(cache_manager: CacheManager, pattern: str):
    """
    Decorator to invalidate cache entries matching pattern after function execution
    
    Args:
        cache_manager: CacheManager instance
        pattern: Pattern to match for cache invalidation
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            # Invalidate cache after successful execution
            await cache_manager.delete_pattern(pattern)
            return result
        return wrapper
    return decorator