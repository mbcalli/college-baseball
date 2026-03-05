"""Configuration management using Pydantic Settings."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="sqlite:///./baseball.db",
        description="Database connection URL",
    )

    # API
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=False, description="Enable auto-reload in development")
    cors_origins_str: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://localhost:5174",
        description="CORS allowed origins (comma-separated or JSON array)",
        alias="CORS_ORIGINS",
    )
    
    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string, JSON array, or return wildcard."""
        import json
        
        if self.cors_origins_str == "*":
            return ["*"]
        
        # Try parsing as JSON array first
        if self.cors_origins_str.startswith("["):
            try:
                origins = json.loads(self.cors_origins_str)
                return [origin.strip() for origin in origins if origin.strip()]
            except json.JSONDecodeError:
                pass
        
        # Fall back to comma-separated
        return [origin.strip() for origin in self.cors_origins_str.split(",") if origin.strip()]

    # Data paths
    data_dir: Path = Field(default=Path("data"), description="Data directory")
    bronze_dir: Path = Field(default=Path("data/bronze"), description="Bronze layer directory")
    silver_dir: Path = Field(default=Path("data/silver"), description="Silver layer directory")
    static_dir: Path = Field(default=Path("data/static"), description="Static files directory")

    # Fangraphs scraping
    fangraphs_base_url: str = Field(
        default="https://www.fangraphs.com",
        description="Fangraphs base URL",
    )
    fangraphs_college_url: str = Field(
        default="https://www.fangraphs.com/leaders/college",
        description="Fangraphs college leaderboard URL",
    )
    fangraphs_timeout: int = Field(default=30, description="Request timeout in seconds")
    fangraphs_user_agent: Optional[str] = Field(
        default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        description="User agent for requests",
    )

    # Season
    current_season: int = Field(default=2026, description="Current season year")

    @property
    def database_path(self) -> Path:
        """Get database file path for SQLite."""
        if self.database_url.startswith("sqlite:///"):
            return Path(self.database_url.replace("sqlite:///", ""))
        return Path("baseball.db")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
