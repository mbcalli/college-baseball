"""Silver layer processing - calculate percentiles from bronze data."""

import logging
from datetime import datetime
from typing import Any, Optional

import pandas as pd
from sqlalchemy import select, func
from sqlalchemy.orm import Session

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
from college_baseball.processing import (
    process_batting_percentiles,
    process_pitching_percentiles,
)

logger = logging.getLogger(__name__)


def ensure_datetime(dt: Any) -> datetime:
    """Convert string datetime to datetime object if needed."""
    if isinstance(dt, str):
        # Remove microseconds if present (e.g., '2025-06-23 00:00:00.000000')
        dt_str = dt.split('.')[0] if '.' in dt else dt
        return datetime.fromisoformat(dt_str.replace(' ', 'T'))
    return dt


class SilverProcessor:
    """Service for processing bronze data into silver layer with percentiles."""

    def __init__(self, session: Session):
        """Initialize processor with database session."""
        self.session = session

    def process_adv_batting(self, data_date: Optional[datetime] = None) -> int:
        """Process advanced batting data and calculate percentiles."""
        logger.info("Processing advanced batting percentiles")
        
        # Get the latest data_date if not specified
        if data_date is None:
            max_date_result = self.session.execute(
                select(func.max(BronzeAdvBatting.data_date))
            ).scalar()
            if max_date_result is None:
                logger.warning("No bronze advanced batting data found")
                return 0
            data_date = max_date_result
        
        # Ensure data_date is a datetime object
        data_date = ensure_datetime(data_date)
        
        # Delete existing silver records for this date (in case we're reprocessing)
        delete_stmt = SilverAdvBatting.__table__.delete().where(
            SilverAdvBatting.data_date == data_date
        )
        self.session.execute(delete_stmt)
        self.session.commit()
        
        # Read bronze data for the specified date
        stmt = select(BronzeAdvBatting).where(BronzeAdvBatting.data_date == data_date)
        results = self.session.execute(stmt).scalars().all()
        
        if not results:
            logger.warning(f"No bronze advanced batting data found for {data_date}")
            return 0
        
        # Convert to DataFrame
        data = [
            {
                "id": r.id,
                "name": r.name,
                "team": r.team,
                "pa": r.pa,
                "bb_rate": r.bb_rate,
                "k_rate": r.k_rate,
                "bb_per_k": r.bb_per_k,
                "avg": r.avg,
                "obp": r.obp,
                "slg": r.slg,
                "ops": r.ops,
                "iso": r.iso,
                "spd": r.spd,
                "babip": r.babip,
                "wsb": r.wsb,
                "wrc": r.wrc,
                "wraa": r.wraa,
                "woba": r.woba,
                "wrc_plus": r.wrc_plus,
            }
            for r in results
        ]
        df = pd.DataFrame(data)
        
        # Calculate percentiles
        df = process_batting_percentiles(df, is_advanced=True)
        
        # Insert new records (no delete - incremental loading)
        # Insert new records with only id, name, team, and percentiles
        percentile_cols = [col for col in df.columns if col.endswith("_percentile")]
        for _, row in df.iterrows():
            record = {
                "id": row["id"],
                "data_date": data_date,
                "name": row["name"],
                "team": row["team"],
            }
            # Add all percentile columns
            for col in percentile_cols:
                record[col] = int(row[col]) if pd.notna(row[col]) else None
            
            obj = SilverAdvBatting(**record)
            self.session.add(obj)
        
        self.session.commit()
        logger.info(f"Processed {len(df)} advanced batting records for {data_date}")
        return len(df)

    def process_std_batting(self, data_date: Optional[datetime] = None) -> int:
        """Process standard batting data and calculate percentiles."""
        logger.info("Processing standard batting percentiles")
        
        # Get the latest data_date if not specified
        if data_date is None:
            max_date_result = self.session.execute(
                select(func.max(BronzeStdBatting.data_date))
            ).scalar()
            if max_date_result is None:
                logger.warning("No bronze standard batting data found")
                return 0
            data_date = max_date_result
        
        # Ensure data_date is a datetime object (SQLite returns strings)
        data_date = ensure_datetime(data_date)
        
        # Delete existing silver records for this date (in case we're reprocessing)
        delete_stmt = SilverStdBatting.__table__.delete().where(
            SilverStdBatting.data_date == data_date
        )
        self.session.execute(delete_stmt)
        self.session.commit()
        
        stmt = select(BronzeStdBatting).where(BronzeStdBatting.data_date == data_date)
        results = self.session.execute(stmt).scalars().all()
        
        if not results:
            logger.warning(f"No bronze standard batting data found for {data_date}")
            return 0
        
        data = [
            {
                "id": r.id,
                "name": r.name,
                "team": r.team,
                "g": r.g,
                "ab": r.ab,
                "pa": r.pa,
                "h": r.h,
                "single": r.single,
                "double": r.double,
                "triple": r.triple,
                "hr": r.hr,
                "r": r.r,
                "rbi": r.rbi,
                "bb": r.bb,
                "ibb": r.ibb,
                "so": r.so,
                "hbp": r.hbp,
                "sf": r.sf,
                "sh": r.sh,
                "gdp": r.gdp,
                "sb": r.sb,
                "cs": r.cs,
                "avg": r.avg,
            }
            for r in results
        ]
        df = pd.DataFrame(data)
        
        df = process_batting_percentiles(df, is_advanced=False)
        
        # Insert new records (no delete - incremental loading)
        percentile_cols = [col for col in df.columns if col.endswith("_percentile")]
        for _, row in df.iterrows():
            record = {
                "id": row["id"],
                "data_date": data_date,
                "name": row["name"],
                "team": row["team"],
            }
            for col in percentile_cols:
                record[col] = int(row[col]) if pd.notna(row[col]) else None
            
            obj = SilverStdBatting(**record)
            self.session.add(obj)
        
        self.session.commit()
        logger.info(f"Processed {len(df)} standard batting records for {data_date}")
        return len(df)

    def process_adv_pitching(self, data_date: Optional[datetime] = None) -> int:
        """Process advanced pitching data and calculate percentiles."""
        logger.info("Processing advanced pitching percentiles")
        
        # Get the latest data_date if not specified
        if data_date is None:
            max_date_result = self.session.execute(
                select(func.max(BronzeAdvPitching.data_date))
            ).scalar()
            if max_date_result is None:
                logger.warning("No bronze advanced pitching data found")
                return 0
            data_date = max_date_result
        
        # Ensure data_date is a datetime object (SQLite returns strings)
        data_date = ensure_datetime(data_date)
        
        # Delete existing silver records for this date (in case we're reprocessing)
        delete_stmt = SilverAdvPitching.__table__.delete().where(
            SilverAdvPitching.data_date == data_date
        )
        self.session.execute(delete_stmt)
        self.session.commit()
        
        stmt = select(BronzeAdvPitching).where(BronzeAdvPitching.data_date == data_date)
        results = self.session.execute(stmt).scalars().all()
        
        if not results:
            logger.warning(f"No bronze advanced pitching data found for {data_date}")
            return 0
        
        data = [
            {
                "id": r.id,
                "name": r.name,
                "team": r.team,
                "w": r.w,
                "l": r.l,
                "sv": r.sv,
                "g": r.g,
                "gs": r.gs,
                "ip": r.ip,
                "k_per_9": r.k_per_9,
                "bb_per_9": r.bb_per_9,
                "hr_per_9": r.hr_per_9,
                "babip": r.babip,
                "lob_pct": r.lob_pct,
                "gb_pct": r.gb_pct,
                "hr_per_fb": r.hr_per_fb,
                "era": r.era,
                "fip": r.fip,
                "xfip": r.xfip,
                "siera": r.siera,
            }
            for r in results
        ]
        df = pd.DataFrame(data)
        
        df = process_pitching_percentiles(df, is_advanced=True)
        
        # Insert new records (no delete - incremental loading)
        percentile_cols = [col for col in df.columns if col.endswith("_percentile")]
        for _, row in df.iterrows():
            record = {
                "id": row["id"],
                "data_date": data_date,
                "name": row["name"],
                "team": row["team"],
            }
            for col in percentile_cols:
                record[col] = int(row[col]) if pd.notna(row[col]) else None
            
            obj = SilverAdvPitching(**record)
            self.session.add(obj)
        
        self.session.commit()
        logger.info(f"Processed {len(df)} advanced pitching records for {data_date}")
        return len(df)

    def process_std_pitching(self, data_date: Optional[datetime] = None) -> int:
        """Process standard pitching data and calculate percentiles."""
        logger.info("Processing standard pitching percentiles")
        
        # Get the latest data_date if not specified
        if data_date is None:
            max_date_result = self.session.execute(
                select(func.max(BronzeStdPitching.data_date))
            ).scalar()
            if max_date_result is None:
                logger.warning("No bronze standard pitching data found")
                return 0
            data_date = max_date_result
        
        # Ensure data_date is a datetime object (SQLite returns strings)
        data_date = ensure_datetime(data_date)
        
        # Delete existing silver records for this date (in case we're reprocessing)
        delete_stmt = SilverStdPitching.__table__.delete().where(
            SilverStdPitching.data_date == data_date
        )
        self.session.execute(delete_stmt)
        self.session.commit()
        
        stmt = select(BronzeStdPitching).where(BronzeStdPitching.data_date == data_date)
        results = self.session.execute(stmt).scalars().all()
        
        if not results:
            logger.warning(f"No bronze standard pitching data found for {data_date}")
            return 0
        
        data = [
            {
                "id": r.id,
                "name": r.name,
                "team": r.team,
                "w": r.w,
                "l": r.l,
                "era": r.era,
                "g": r.g,
                "gs": r.gs,
                "cg": r.cg,
                "sho": r.sho,
                "sv": r.sv,
                "ip": r.ip,
                "h": r.h,
                "r": r.r,
                "er": r.er,
                "hr": r.hr,
                "bb": r.bb,
                "ibb": r.ibb,
                "hbp": r.hbp,
                "wp": r.wp,
                "bk": r.bk,
                "so": r.so,
            }
            for r in results
        ]
        df = pd.DataFrame(data)
        
        df = process_pitching_percentiles(df, is_advanced=False)
        
        # Insert new records (no delete - incremental loading)
        percentile_cols = [col for col in df.columns if col.endswith("_percentile")]
        for _, row in df.iterrows():
            record = {
                "id": row["id"],
                "data_date": data_date,
                "name": row["name"],
                "team": row["team"],
            }
            for col in percentile_cols:
                record[col] = int(row[col]) if pd.notna(row[col]) else None
            
            obj = SilverStdPitching(**record)
            self.session.add(obj)
        
        self.session.commit()
        logger.info(f"Processed {len(df)} standard pitching records for {data_date}")
        return len(df)

    def process_all(self, data_date: Optional[datetime] = None) -> dict[str, int]:
        """Process all bronze data into silver layer."""
        results = {}
        
        results["adv_batting"] = self.process_adv_batting(data_date)
        results["std_batting"] = self.process_std_batting(data_date)
        results["adv_pitching"] = self.process_adv_pitching(data_date)
        results["std_pitching"] = self.process_std_pitching(data_date)
        
        return results
