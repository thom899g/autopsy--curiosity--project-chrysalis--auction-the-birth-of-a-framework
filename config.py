"""
Configuration management for Project CHRYSALIS auction framework.
Centralized configuration with environment variable fallbacks and validation.
"""
import os
from typing import Dict, Optional, Any
from dataclasses import dataclass
import logging

@dataclass
class AuctionConfig:
    """Configuration for auction system parameters."""
    # Firebase configuration
    firebase_project_id: str
    firestore_collection_prefix: str = "auctions"
    
    # Auction parameters
    minimum_bid_increment: float = 0.01
    auction_duration_hours: int = 24
    reserve_price: Optional[float] = None
    
    # Notification settings
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    
    # Logging configuration
    log_level: str = "INFO"
    log_file: Optional[str] = "auction_system.log"
    
    @classmethod
    def from_env(cls) -> 'AuctionConfig':
        """Load configuration from environment variables."""
        return cls(
            firebase_project_id=os.getenv("FIREBASE_PROJECT_ID", "chrysalis-auctions"),
            firestore_collection_prefix=os.getenv("FIRESTORE_PREFIX", "auctions"),
            minimum_bid_increment=float(os.getenv("MIN_BID_INCREMENT", "0.01")),
            auction_duration_hours=int(os.getenv("AUCTION_DURATION_HOURS", "24")),
            reserve_price=float(os.getenv("RESERVE_PRICE")) if os.getenv("RESERVE_PRICE") else None,
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE")
        )

class ConfigManager:
    """Manages configuration with validation and hot-reload capability."""
    
    def __init__(self):
        self.config: AuctionConfig = AuctionConfig.from_env()
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate configuration values."""
        if not self.config.firebase_project_id:
            raise ValueError("FIREBASE_PROJECT_ID is required")
        
        if self.config.minimum_bid_increment <= 0:
            raise ValueError("minimum_bid_increment must be positive")
        
        if self.config.auction_duration_hours <= 0:
            raise ValueError("auction_duration_hours must be positive")
    
    def reload(self) -> None:
        """Reload configuration from environment."""
        self.config = AuctionConfig.from_env()
        self._validate_config()

# Global configuration instance
config_manager = ConfigManager()
CONFIG = config_manager.config