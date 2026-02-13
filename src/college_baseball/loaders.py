"""Data loading services for bronze layer."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from college_baseball.models import (
    BronzeAdvBatting,
    BronzeAdvPitching,
    BronzeStdBatting,
    BronzeStdPitching,
)

logger = logging.getLogger(__name__)


def clean_numeric_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace inf and NaN values with None for proper database handling."""
    # Replace inf with NaN first
    df = df.replace([np.inf, -np.inf], np.nan)
    
    # Convert to object dtype to allow None values, then replace NaN with None
    for col in df.columns:
        if df[col].dtype in ['float64', 'float32', 'int64', 'int32']:
            df[col] = df[col].astype('object').where(pd.notnull(df[col]), None)
    
    return df


class DataLoader:
    """Service for loading CSV data into bronze layer."""

    def __init__(self, session: Session):
        """Initialize data loader with database session."""
        self.session = session

    def load_adv_batting(self, csv_path: Path, data_date: Optional[datetime] = None) -> int:
        """Load advanced batting data from CSV."""
        logger.info(f"Loading advanced batting data from {csv_path}")
        
        if data_date is None:
            data_date = datetime.utcnow()
        
        df = pd.read_csv(csv_path)
        
        # Drop columns we don't need
        columns_to_drop = ["MLBAMID", "NameASCII"]
        for col in columns_to_drop:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        # Rename columns to match model
        column_map = {
            "Name": "name",
            "Team": "team",
            "Age": "age",
            "PA": "pa",
            "BB%": "bb_rate",
            "K%": "k_rate",
            "BB/K": "bb_per_k",
            "AVG": "avg",
            "OBP": "obp",
            "SLG": "slg",
            "OPS": "ops",
            "ISO": "iso",
            "Spd": "spd",
            "BABIP": "babip",
            "wSB": "wsb",
            "wRC": "wrc",
            "wRAA": "wraa",
            "wOBA": "woba",
            "wRC+": "wrc_plus",
            "PlayerId": "id",  # Map PlayerId to id
        }
        
        # Add alt_name if it exists
        if "alt_name" in df.columns:
            column_map["alt_name"] = "alt_name"
        
        df = df.rename(columns=column_map)
        
        # Clean numeric values (replace inf/NaN with None)
        df = clean_numeric_values(df)
        
        # Insert new records (no delete - incremental loading)
        records = df.to_dict("records")
        for record in records:
            record["data_date"] = data_date
            obj = BronzeAdvBatting(**record)
            self.session.add(obj)
        
        self.session.commit()
        logger.info(f"Loaded {len(records)} advanced batting records for {data_date}")
        return len(records)

    def load_std_batting(self, csv_path: Path, data_date: Optional[datetime] = None) -> int:
        """Load standard batting data from CSV."""
        logger.info(f"Loading standard batting data from {csv_path}")
        
        if data_date is None:
            data_date = datetime.utcnow()
        
        df = pd.read_csv(csv_path)
        
        # Drop columns we don't need
        columns_to_drop = ["MLBAMID", "NameASCII"]
        for col in columns_to_drop:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        column_map = {
            "Name": "name",
            "Team": "team",
            "Age": "age",
            "G": "g",
            "AB": "ab",
            "PA": "pa",
            "H": "h",
            "1B": "single",
            "2B": "double",
            "3B": "triple",
            "HR": "hr",
            "R": "r",
            "RBI": "rbi",
            "BB": "bb",
            "IBB": "ibb",
            "SO": "so",
            "HBP": "hbp",
            "SF": "sf",
            "SH": "sh",
            "GDP": "gdp",
            "SB": "sb",
            "CS": "cs",
            "AVG": "avg",
            "PlayerId": "id",  # Map PlayerId to id
        }
        
        if "alt_name" in df.columns:
            column_map["alt_name"] = "alt_name"
        
        df = df.rename(columns=column_map)
        
        # Clean numeric values (replace inf/NaN with None)
        df = clean_numeric_values(df)
        
        # Insert new records (no delete - incremental loading)
        records = df.to_dict("records")
        for record in records:
            record["data_date"] = data_date
            obj = BronzeStdBatting(**record)
            self.session.add(obj)
        
        self.session.commit()
        logger.info(f"Loaded {len(records)} standard batting records for {data_date}")
        return len(records)

    def load_adv_pitching(self, csv_path: Path, data_date: Optional[datetime] = None) -> int:
        """Load advanced pitching data from CSV."""
        logger.info(f"Loading advanced pitching data from {csv_path}")
        
        if data_date is None:
            data_date = datetime.utcnow()
        
        df = pd.read_csv(csv_path)
        
        # Drop columns we don't need or don't have in model
        columns_to_drop = ["MLBAMID", "NameASCII", "K/BB", "K%", "BB%", "K-BB%", "AVG", "WHIP", "E-F", "GB%", "HR/FB", "xFIP", "SIERA"]
        for col in columns_to_drop:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        column_map = {
            "Name": "name",
            "Team": "team",
            "Age": "age",
            "IP": "ip",
            "K/9": "k_per_9",
            "BB/9": "bb_per_9",
            "HR/9": "hr_per_9",
            "BABIP": "babip",
            "LOB%": "lob_pct",
            "ERA": "era",
            "FIP": "fip",
            "PlayerId": "id",  # Map PlayerId to id
        }
        
        if "alt_name" in df.columns:
            column_map["alt_name"] = "alt_name"
        
        df = df.rename(columns=column_map)
        
        # Clean numeric values (replace inf/NaN with None)
        df = clean_numeric_values(df)
        
        # Insert new records (no delete - incremental loading)
        records = df.to_dict("records")
        for record in records:
            record["data_date"] = data_date
            obj = BronzeAdvPitching(**record)
            self.session.add(obj)
        
        self.session.commit()
        logger.info(f"Loaded {len(records)} advanced pitching records for {data_date}")
        return len(records)

    def load_std_pitching(self, csv_path: Path, data_date: Optional[datetime] = None) -> int:
        """Load standard pitching data from CSV."""
        logger.info(f"Loading standard pitching data from {csv_path}")
        
        if data_date is None:
            data_date = datetime.utcnow()
        
        df = pd.read_csv(csv_path)
        
        # Drop columns we don't need or don't have in model
        columns_to_drop = ["MLBAMID", "NameASCII", "TBF"]
        for col in columns_to_drop:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        column_map = {
            "Name": "name",
            "Team": "team",
            "Age": "age",
            "W": "w",
            "L": "l",
            "ERA": "era",
            "G": "g",
            "GS": "gs",
            "CG": "cg",
            "ShO": "sho",
            "SV": "sv",
            "IP": "ip",
            "H": "h",
            "R": "r",
            "ER": "er",
            "HR": "hr",
            "BB": "bb",
            "HBP": "hbp",
            "WP": "wp",
            "BK": "bk",
            "SO": "so",
            "PlayerId": "id",  # Map PlayerId to id
        }
        
        if "alt_name" in df.columns:
            column_map["alt_name"] = "alt_name"
        
        df = df.rename(columns=column_map)
        
        # Clean numeric values (replace inf/NaN with None)
        df = clean_numeric_values(df)
        
        # Insert new records (no delete - incremental loading)
        records = df.to_dict("records")
        for record in records:
            record["data_date"] = data_date
            obj = BronzeStdPitching(**record)
            self.session.add(obj)
        
        self.session.commit()
        logger.info(f"Loaded {len(records)} standard pitching records for {data_date}")
        return len(records)

    def load_all(self, data_dir: Path, data_date: Optional[datetime] = None) -> dict[str, int]:
        """Load all CSV files from data directory."""
        results = {}
        
        files = {
            "adv_batting": data_dir / "adv_batting.csv",
            "std_batting": data_dir / "std_batting.csv",
            "adv_pitching": data_dir / "adv_pitching.csv",
            "std_pitching": data_dir / "std_pitching.csv",
        }
        
        for name, path in files.items():
            if not path.exists():
                logger.warning(f"File not found: {path}")
                continue
            
            if name == "adv_batting":
                results[name] = self.load_adv_batting(path, data_date)
            elif name == "std_batting":
                results[name] = self.load_std_batting(path, data_date)
            elif name == "adv_pitching":
                results[name] = self.load_adv_pitching(path, data_date)
            elif name == "std_pitching":
                results[name] = self.load_std_pitching(path, data_date)
        
        return results
