"""FastAPI application and API endpoints."""

import logging
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from college_baseball import __version__
from college_baseball.config import get_settings
from college_baseball.database import get_db, init_db
from college_baseball.models import (
    BronzeAdvBatting,
    BronzeAdvPitching,
    BronzeStdBatting,
    BronzeStdPitching,
    SilverAdvBatting,
    SilverAdvPitching,
    SilverStdBatting,
    SilverStdPitching,
)
from college_baseball.schemas import (
    DataDateInfo,
    DataDatesResponse,
    ErrorResponse,
    HealthResponse,
    MetricDefinition,
    MetricsResponse,
    PlayerProfile,
    PlayerStatistic,
    TeamComparison,
    TeamPlayer,
    TeamRoster,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()
logger.info(f"CORS origins configured: {settings.cors_origins}")

# Create FastAPI app
app = FastAPI(
    title="College Baseball Statistics API",
    description="API for college baseball statistics with percentile-based rankings",
    version=__version__,
)

# Add CORS middleware
logger.info(f"Adding CORS middleware with origins: {settings.cors_origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_latest_data_date_batting(db: Session, year: Optional[int] = None):
    """Get the latest data_date from batting tables, optionally filtered by year."""
    if year:
        # Get max date for specific year
        max_date = db.execute(
            select(func.max(BronzeAdvBatting.data_date))
            .where(func.extract('year', BronzeAdvBatting.data_date) == year)
        ).scalar()
    else:
        # Get overall max date
        max_date = db.execute(select(func.max(BronzeAdvBatting.data_date))).scalar()
    return max_date


def get_latest_data_date_pitching(db: Session, year: Optional[int] = None):
    """Get the latest data_date from pitching tables, optionally filtered by year."""
    if year:
        # Get max date for specific year
        max_date = db.execute(
            select(func.max(BronzeAdvPitching.data_date))
            .where(func.extract('year', BronzeAdvPitching.data_date) == year)
        ).scalar()
    else:
        # Get overall max date
        max_date = db.execute(select(func.max(BronzeAdvPitching.data_date))).scalar()
    return max_date


def get_available_years(db: Session) -> list[int]:
    """Get list of available years from the data."""
    batting_years = db.execute(
        select(func.distinct(func.extract('year', BronzeAdvBatting.data_date)))
        .order_by(func.extract('year', BronzeAdvBatting.data_date).desc())
    ).scalars().all()
    return [int(year) for year in batting_years if year]


# Removed startup event for Lambda - database is already initialized
# @app.on_event("startup")
# def startup_event() -> None:
#     """Initialize database on startup."""
#     logger.info("Initializing database...")
#     init_db()
#     logger.info("Database initialized")


@app.get("/", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    """Health check endpoint."""
    try:
        # Test database connection
        db.execute(select(1))
        database_connected = True
    except Exception:
        database_connected = False
    
    return HealthResponse(
        status="healthy" if database_connected else "unhealthy",
        version=__version__,
        database_connected=database_connected,
    )


@app.get("/api/teams", response_model=list[str])
def get_teams(
    year: Optional[int] = Query(None, description="Filter by year (e.g., 2025, 2026)"),
    db: Session = Depends(get_db)
) -> list[str]:
    """Get list of all teams."""
    latest_date = get_latest_data_date_batting(db, year)
    if latest_date is None:
        return []
    stmt = (
        select(BronzeAdvBatting.team)
        .where(BronzeAdvBatting.data_date == latest_date)
        .distinct()
        .order_by(BronzeAdvBatting.team)
    )
    teams = db.execute(stmt).scalars().all()
    return list(teams)


@app.get("/api/years", response_model=list[int])
def get_years(db: Session = Depends(get_db)) -> list[int]:
    """Get list of available years in the data."""
    return get_available_years(db)


@app.get("/api/data-dates", response_model=DataDatesResponse)
def get_data_dates(db: Session = Depends(get_db)) -> DataDatesResponse:
    """Get last update date for each available year."""
    years = get_available_years(db)
    year_info = []
    
    for year in years:
        # Get max date for this year from batting data
        max_date = db.execute(
            select(func.max(BronzeAdvBatting.data_date))
            .where(func.extract('year', BronzeAdvBatting.data_date) == year)
        ).scalar()
        
        if max_date:
            year_info.append(DataDateInfo(
                year=year,
                last_update=max_date.strftime('%Y-%m-%d')
            ))
    
    return DataDatesResponse(years=year_info)


@app.get("/api/teams/{team}/roster", response_model=TeamRoster)
def get_team_roster(
    team: str,
    year: Optional[int] = Query(None, description="Filter by year (e.g., 2025, 2026)"),
    db: Session = Depends(get_db)
) -> TeamRoster:
    """Get team roster with batters and pitchers."""
    latest_batting_date = get_latest_data_date_batting(db, year)
    latest_pitching_date = get_latest_data_date_pitching(db, year)
    
    # Get batters
    if latest_batting_date:
        batter_stmt = (
            select(BronzeAdvBatting.name)
            .where(BronzeAdvBatting.team == team, BronzeAdvBatting.data_date == latest_batting_date)
            .distinct()
            .order_by(BronzeAdvBatting.name)
        )
        batters = db.execute(batter_stmt).scalars().all()
    else:
        batters = []
    
    # Get pitchers
    if latest_pitching_date:
        pitcher_stmt = (
            select(BronzeAdvPitching.name)
            .where(BronzeAdvPitching.team == team, BronzeAdvPitching.data_date == latest_pitching_date)
            .distinct()
            .order_by(BronzeAdvPitching.name)
        )
        pitchers = db.execute(pitcher_stmt).scalars().all()
    else:
        pitchers = []
    
    return TeamRoster(team=team, batters=list(batters), pitchers=list(pitchers))


def format_value(value: Optional[float]) -> str:
    """Format a numeric value for display."""
    if value is None:
        return "N/A"
    if value > 10:
        return f"{value:.0f}"
    if value > 5:
        return f"{value:.1f}"
    if value > 1:
        return f"{value:.2f}"
    return f"{value:.3f}"


@app.get("/api/players/{player_name}/batting", response_model=PlayerProfile)
def get_player_batting(
    player_name: str,
    advanced: bool = Query(True, description="Use advanced stats"),
    year: Optional[int] = Query(None, description="Filter by year (e.g., 2025, 2026)"),
    db: Session = Depends(get_db),
) -> PlayerProfile:
    """Get batting statistics for a player."""
    latest_date = get_latest_data_date_batting(db, year)
    if latest_date is None:
        raise HTTPException(status_code=404, detail="No batting data available")
    
    if advanced:
        # Get bronze and silver data
        bronze_stmt = select(BronzeAdvBatting).where(
            BronzeAdvBatting.name == player_name,
            BronzeAdvBatting.data_date == latest_date
        )
        bronze = db.execute(bronze_stmt).scalar_one_or_none()
        
        if not bronze:
            raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")
        
        silver_stmt = select(SilverAdvBatting).where(
            SilverAdvBatting.id == bronze.id,
            SilverAdvBatting.data_date == latest_date
        )
        silver = db.execute(silver_stmt).scalar_one_or_none()
        
        if not silver:
            raise HTTPException(status_code=404, detail=f"Percentile data not found for '{player_name}'")
        
        # Build statistics list
        stats = [
            ("PA", bronze.pa, silver.pa_percentile),
            ("BB%", bronze.bb_rate, silver.bb_rate_percentile),
            ("K%", bronze.k_rate, silver.k_rate_percentile),
            ("BB/K", bronze.bb_per_k, silver.bb_per_k_percentile),
            ("AVG", bronze.avg, silver.avg_percentile),
            ("OBP", bronze.obp, silver.obp_percentile),
            ("SLG", bronze.slg, silver.slg_percentile),
            ("OPS", bronze.ops, silver.ops_percentile),
            ("ISO", bronze.iso, silver.iso_percentile),
            ("Spd", bronze.spd, silver.spd_percentile),
            ("BABIP", bronze.babip, silver.babip_percentile),
            ("wSB", bronze.wsb, silver.wsb_percentile),
            ("wRC", bronze.wrc, silver.wrc_percentile),
            ("wRAA", bronze.wraa, silver.wraa_percentile),
            ("wOBA", bronze.woba, silver.woba_percentile),
            ("wRC+", bronze.wrc_plus, silver.wrc_plus_percentile),
        ]
    else:
        bronze_stmt = select(BronzeStdBatting).where(
            BronzeStdBatting.name == player_name,
            BronzeStdBatting.data_date == latest_date
        )
        bronze = db.execute(bronze_stmt).scalar_one_or_none()
        
        if not bronze:
            raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")
        
        silver_stmt = select(SilverStdBatting).where(
            SilverStdBatting.id == bronze.id,
            SilverStdBatting.data_date == latest_date
        )
        silver = db.execute(silver_stmt).scalar_one_or_none()
        
        if not silver:
            raise HTTPException(status_code=404, detail=f"Percentile data not found for '{player_name}'")
        
        stats = [
            ("G", bronze.g, silver.g_percentile),
            ("AB", bronze.ab, silver.ab_percentile),
            ("PA", bronze.pa, silver.pa_percentile),
            ("H", bronze.h, silver.h_percentile),
            ("1B", bronze.single, silver.single_percentile),
            ("2B", bronze.double, silver.double_percentile),
            ("3B", bronze.triple, silver.triple_percentile),
            ("HR", bronze.hr, silver.hr_percentile),
            ("R", bronze.r, silver.r_percentile),
            ("RBI", bronze.rbi, silver.rbi_percentile),
            ("BB", bronze.bb, silver.bb_percentile),
            ("SO", bronze.so, silver.so_percentile),
            ("SB", bronze.sb, silver.sb_percentile),
            ("AVG", bronze.avg, silver.avg_percentile),
        ]
    
    statistics = [
        PlayerStatistic(
            name=name,
            value=value if value is not None else 0,
            percentile=percentile if percentile is not None else 0,
            formatted_value=format_value(value),
        )
        for name, value, percentile in stats
    ]
    
    return PlayerProfile(
        id=bronze.id,
        name=bronze.name,
        team=bronze.team,
        statistics=statistics,
        stat_type="batting",
        is_advanced=advanced,
    )


@app.get("/api/players/{player_name}/pitching", response_model=PlayerProfile)
def get_player_pitching(
    player_name: str,
    advanced: bool = Query(True, description="Use advanced stats"),
    year: Optional[int] = Query(None, description="Filter by year (e.g., 2025, 2026)"),
    db: Session = Depends(get_db),
) -> PlayerProfile:
    """Get pitching statistics for a player."""
    latest_date = get_latest_data_date_pitching(db, year)
    if latest_date is None:
        raise HTTPException(status_code=404, detail="No pitching data available")
    
    if advanced:
        bronze_stmt = select(BronzeAdvPitching).where(
            BronzeAdvPitching.name == player_name,
            BronzeAdvPitching.data_date == latest_date
        )
        bronze = db.execute(bronze_stmt).scalar_one_or_none()
        
        if not bronze:
            raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")
        
        silver_stmt = select(SilverAdvPitching).where(
            SilverAdvPitching.id == bronze.id,
            SilverAdvPitching.data_date == latest_date
        )
        silver = db.execute(silver_stmt).scalar_one_or_none()
        
        if not silver:
            raise HTTPException(status_code=404, detail=f"Percentile data not found for '{player_name}'")
        
        stats = [
            ("IP", bronze.ip, silver.ip_percentile),
            ("K/9", bronze.k_per_9, silver.k_per_9_percentile),
            ("BB/9", bronze.bb_per_9, silver.bb_per_9_percentile),
            ("HR/9", bronze.hr_per_9, silver.hr_per_9_percentile),
            ("BABIP", bronze.babip, silver.babip_percentile),
            ("LOB%", bronze.lob_pct, silver.lob_pct_percentile),
            ("GB%", bronze.gb_pct, silver.gb_pct_percentile),
            ("ERA", bronze.era, silver.era_percentile),
            ("FIP", bronze.fip, silver.fip_percentile),
            ("xFIP", bronze.xfip, silver.xfip_percentile),
            ("SIERA", bronze.siera, silver.siera_percentile),
        ]
    else:
        bronze_stmt = select(BronzeStdPitching).where(
            BronzeStdPitching.name == player_name,
            BronzeStdPitching.data_date == latest_date
        )
        bronze = db.execute(bronze_stmt).scalar_one_or_none()
        
        if not bronze:
            raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")
        
        silver_stmt = select(SilverStdPitching).where(
            SilverStdPitching.id == bronze.id,
            SilverStdPitching.data_date == latest_date
        )
        silver = db.execute(silver_stmt).scalar_one_or_none()
        
        if not silver:
            raise HTTPException(status_code=404, detail=f"Percentile data not found for '{player_name}'")
        
        stats = [
            ("W", bronze.w, silver.w_percentile),
            ("L", bronze.l, silver.l_percentile),
            ("ERA", bronze.era, silver.era_percentile),
            ("G", bronze.g, silver.g_percentile),
            ("IP", bronze.ip, silver.ip_percentile),
            ("SO", bronze.so, silver.so_percentile),
        ]
    
    statistics = [
        PlayerStatistic(
            name=name,
            value=value if value is not None else 0,
            percentile=percentile if percentile is not None else 0,
            formatted_value=format_value(value),
        )
        for name, value, percentile in stats
    ]
    
    return PlayerProfile(
        id=bronze.id,
        name=bronze.name,
        team=bronze.team,
        statistics=statistics,
        stat_type="pitching",
        is_advanced=advanced,
    )


@app.get("/api/metrics", response_model=MetricsResponse)
def get_metrics() -> MetricsResponse:
    """Get all available metrics and their descriptions."""
    metrics = {
        # Batting - Advanced
        "PA": MetricDefinition(name="PA", description="Plate appearances", higher_is_better=True),
        "BB%": MetricDefinition(name="BB%", description="Walk rate (BB/PA)", higher_is_better=True),
        "K%": MetricDefinition(name="K%", description="Strikeout rate (K/PA)", higher_is_better=False),
        "wRC+": MetricDefinition(name="wRC+", description="League-adjusted wRC (100 = average)", higher_is_better=True),
        # Add more as needed...
    }
    
    return MetricsResponse(metrics=metrics)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "college_baseball.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )


# Lambda handler for AWS Lambda deployment
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off", api_gateway_base_path="/default")
except ImportError:
    # Mangum not installed, skip Lambda handler
    pass
