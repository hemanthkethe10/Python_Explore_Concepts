"""
Configuration settings for the tick-based notification system.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """Application configuration."""
    
    # MongoDB settings
    mongodb_uri: str = field(
        default_factory=lambda: os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    )
    mongodb_database: str = field(
        default_factory=lambda: os.getenv("MONGODB_DATABASE", "notifications_db")
    )
    
    # Ticker settings
    tick_interval_seconds: int = 60  # How often the ticker runs
    
    # Worker settings
    worker_count: int = field(
        default_factory=lambda: int(os.getenv("WORKER_COUNT", "3"))
    )
    max_retries: int = 3
    retry_delay_seconds: int = 5
    
    # Queue settings
    queue_type: str = field(
        default_factory=lambda: os.getenv("QUEUE_TYPE", "memory")  # memory, redis, sqs
    )
    redis_url: Optional[str] = field(
        default_factory=lambda: os.getenv("REDIS_URL")
    )
    
    # Notification settings (for demo)
    smtp_host: Optional[str] = field(default_factory=lambda: os.getenv("SMTP_HOST"))
    smtp_port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "587")))
    smtp_user: Optional[str] = field(default_factory=lambda: os.getenv("SMTP_USER"))
    smtp_password: Optional[str] = field(default_factory=lambda: os.getenv("SMTP_PASSWORD"))


# Global config instance
config = Config()

