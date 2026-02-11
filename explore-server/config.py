#!/usr/bin/env python3
"""
Configuration management for Explore Server
Loads configuration from environment variables with defaults
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class with environment variable support"""
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # Rate Limiting Configuration
    DEFAULT_RATE_LIMIT: str = os.getenv("DEFAULT_RATE_LIMIT", "10/minute")
    STRICT_RATE_LIMIT: str = os.getenv("STRICT_RATE_LIMIT", "5/minute")
    LOOSE_RATE_LIMIT: str = os.getenv("LOOSE_RATE_LIMIT", "50/minute")
    GRAPHQL_RATE_LIMIT: str = os.getenv("GRAPHQL_RATE_LIMIT", "15/minute")
    
    # Rate Limit Response Configuration
    RETRY_AFTER_SECONDS: int = int(os.getenv("RETRY_AFTER_SECONDS", "60"))
    RATE_LIMIT_MESSAGE: str = os.getenv("RATE_LIMIT_MESSAGE", "Rate limit exceeded")
    
    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "True").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # API Configuration
    API_TITLE: str = os.getenv("API_TITLE", "Explore Server")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "FastAPI server with rate limiting, REST API, and GraphQL endpoints")
    
    # GraphQL Configuration
    GRAPHQL_PLAYGROUND_ENABLED: bool = os.getenv("GRAPHQL_PLAYGROUND_ENABLED", "True").lower() == "true"
    GRAPHQL_INTROSPECTION_ENABLED: bool = os.getenv("GRAPHQL_INTROSPECTION_ENABLED", "True").lower() == "true"
    
    # Slow Operation Configuration
    MAX_SLOW_OPERATION_DELAY: int = int(os.getenv("MAX_SLOW_OPERATION_DELAY", "10"))
    
    # Cache Configuration
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TTL: int = int(os.getenv("CACHE_DEFAULT_TTL", "300"))  # 5 minutes
    CACHE_STATS_TTL: int = int(os.getenv("CACHE_STATS_TTL", "60"))      # 1 minute
    CACHE_USERS_TTL: int = int(os.getenv("CACHE_USERS_TTL", "180"))     # 3 minutes
    CACHE_POSTS_TTL: int = int(os.getenv("CACHE_POSTS_TTL", "120"))     # 2 minutes
    CACHE_RATE_LIMIT_INFO_TTL: int = int(os.getenv("CACHE_RATE_LIMIT_INFO_TTL", "3600"))  # 1 hour
    
    @classmethod
    def get_rate_limits(cls) -> Dict[str, str]:
        """Get all rate limit configurations"""
        return {
            "default": cls.DEFAULT_RATE_LIMIT,
            "strict": cls.STRICT_RATE_LIMIT,
            "loose": cls.LOOSE_RATE_LIMIT,
            "graphql": cls.GRAPHQL_RATE_LIMIT
        }
    
    @classmethod
    def get_cors_config(cls) -> Dict[str, Any]:
        """Get CORS configuration"""
        return {
            "allow_origins": cls.CORS_ORIGINS,
            "allow_credentials": cls.CORS_ALLOW_CREDENTIALS,
            "allow_methods": ["*"],
            "allow_headers": ["*"]
        }
    
    @classmethod
    def get_server_config(cls) -> Dict[str, Any]:
        """Get server configuration for uvicorn"""
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "reload": cls.RELOAD,
            "log_level": cls.LOG_LEVEL
        }
    
    @classmethod
    def get_cache_config(cls) -> Dict[str, Any]:
        """Get cache configuration"""
        return {
            "enabled": cls.CACHE_ENABLED,
            "redis_url": cls.REDIS_URL if cls.CACHE_ENABLED else None,
            "default_ttl": cls.CACHE_DEFAULT_TTL,
            "ttl_settings": {
                "stats": cls.CACHE_STATS_TTL,
                "users": cls.CACHE_USERS_TTL,
                "posts": cls.CACHE_POSTS_TTL,
                "rate_limit_info": cls.CACHE_RATE_LIMIT_INFO_TTL
            }
        }
    
    @classmethod
    def print_config(cls):
        """Print current configuration (for debugging)"""
        print("=" * 50)
        print("EXPLORE SERVER CONFIGURATION")
        print("=" * 50)
        print(f"Host: {cls.HOST}")
        print(f"Port: {cls.PORT}")
        print(f"Debug: {cls.DEBUG}")
        print(f"Reload: {cls.RELOAD}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Default Rate Limit: {cls.DEFAULT_RATE_LIMIT}")
        print(f"GraphQL Rate Limit: {cls.GRAPHQL_RATE_LIMIT}")
        print(f"Retry After: {cls.RETRY_AFTER_SECONDS} seconds")
        print(f"CORS Origins: {cls.CORS_ORIGINS}")
        print(f"GraphQL Playground: {cls.GRAPHQL_PLAYGROUND_ENABLED}")
        print(f"Cache Enabled: {cls.CACHE_ENABLED}")
        if cls.CACHE_ENABLED:
            print(f"Redis URL: {cls.REDIS_URL}")
            print(f"Default Cache TTL: {cls.CACHE_DEFAULT_TTL}s")
        print("=" * 50)

# Create a global config instance
config = Config()