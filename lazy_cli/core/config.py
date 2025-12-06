"""
Configuration management for lazy-cli.
Handles reading and writing user configuration files.
"""

from pathlib import Path
from typing import Any, Optional
import yaml
from pydantic import BaseModel, Field


class LazyConfig(BaseModel):
    """Configuration model for lazy-cli."""
    
    # General settings
    verbose: bool = Field(default=False, description="Enable verbose output")
    
    # Common paths
    default_downloads_folder: Optional[Path] = Field(
        default=None,
        description="Default Downloads folder path"
    )
    default_backup_destination: Optional[Path] = Field(
        default=None,
        description="Default backup destination path"
    )
    
    # Plugin-specific settings
    stock_watchlist: list[str] = Field(
        default_factory=list,
        description="Stock symbols to watch"
    )
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True


def get_config_path() -> Path:
    """
    Get the path to the configuration file.
    
    Returns:
        Path to the config file (~/.lazy-cli/config.yaml)
    """
    config_dir = Path.home() / ".lazy-cli"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.yaml"


def load_config() -> LazyConfig:
    """
    Load configuration from file or create default.
    
    Returns:
        LazyConfig instance
    """
    config_path = get_config_path()
    
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f) or {}
            return LazyConfig(**config_data)
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
            return LazyConfig()
    
    # Create default config
    config = LazyConfig()
    save_config(config)
    return config


def save_config(config: LazyConfig) -> None:
    """
    Save configuration to file.
    
    Args:
        config: LazyConfig instance to save
    """
    config_path = get_config_path()
    
    try:
        with open(config_path, "w") as f:
            yaml.safe_dump(
                config.model_dump(exclude_none=True),
                f,
                default_flow_style=False,
                sort_keys=False,
            )
    except Exception as e:
        print(f"Warning: Could not save config: {e}")


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a single configuration value.
    
    Args:
        key: Configuration key
        default: Default value if key not found
    
    Returns:
        Configuration value or default
    """
    config = load_config()
    return getattr(config, key, default)


def set_config_value(key: str, value: Any) -> None:
    """
    Set a single configuration value.
    
    Args:
        key: Configuration key
        value: Value to set
    """
    config = load_config()
    setattr(config, key, value)
    save_config(config)
