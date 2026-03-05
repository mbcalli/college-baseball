"""Pydantic schemas for API responses."""

from typing import Optional

from pydantic import BaseModel, Field


class PlayerBase(BaseModel):
    """Base player information."""

    id: str
    name: str
    team: str


class PlayerStatistic(BaseModel):
    """Single statistic with value and percentile."""

    name: str = Field(..., description="Statistic name (e.g., 'AVG', 'ERA')")
    value: float = Field(..., description="Raw statistic value")
    percentile: int = Field(..., ge=0, le=100, description="Percentile ranking (0-100)")
    formatted_value: str = Field(..., description="Formatted value for display")


class PlayerProfile(PlayerBase):
    """Complete player profile with all statistics."""

    statistics: list[PlayerStatistic]
    stat_type: str = Field(..., description="Type of stats: 'batting' or 'pitching'")
    is_advanced: bool = Field(..., description="Whether stats are advanced metrics")


class TeamPlayer(BaseModel):
    """Player with single statistic for team comparison."""

    name: str
    value: float
    percentile: int = Field(..., ge=0, le=100)
    formatted_value: str


class TeamComparison(BaseModel):
    """Team comparison for a specific statistic."""

    team: str
    stat_name: str
    stat_display_name: str
    players: list[TeamPlayer]
    min_threshold: Optional[int] = Field(None, description="Minimum PA or IP threshold")


class TeamRoster(BaseModel):
    """Team roster."""

    team: str
    batters: list[str]
    pitchers: list[str]


class MetricDefinition(BaseModel):
    """Metric definition."""

    name: str
    description: str
    higher_is_better: bool = Field(..., description="Whether higher values are better")


class MetricsResponse(BaseModel):
    """Collection of metric definitions."""

    metrics: dict[str, MetricDefinition]


class DataDateInfo(BaseModel):
    """Data date information for a specific year."""

    year: int
    last_update: str = Field(..., description="Last update date in YYYY-MM-DD format")


class DataDatesResponse(BaseModel):
    """Response containing last update dates for all years."""

    years: list[DataDateInfo]


class HealthResponse(BaseModel):
    """API health check response."""

    status: str
    version: str
    database_connected: bool


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: Optional[str] = None
