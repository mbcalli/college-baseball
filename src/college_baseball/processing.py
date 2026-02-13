"""Data processing utilities for calculating percentiles."""

from typing import Sequence

import numpy as np
import pandas as pd


def calculate_percentiles(
    values: Sequence[float],
    invert: bool = False,
) -> list[int]:
    """
    Calculate percentile rankings for a sequence of values.
    
    Args:
        values: Sequence of numeric values
        invert: If True, lower values get higher percentiles (e.g., for ERA, K%)
        
    Returns:
        List of percentile values (0-100)
    """
    series = pd.Series(values)
    
    # Apply inversion if needed
    if invert:
        series = -1 * series
    
    # Calculate percentile rank
    percentiles = series.rank(pct=True, method='average') * 100
    
    # Convert to integers
    return percentiles.astype(int).tolist()


def calculate_all_percentiles(
    df: pd.DataFrame,
    columns: list[str],
    inverted_columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Calculate percentiles for multiple columns in a DataFrame.
    
    Args:
        df: Input DataFrame
        columns: List of column names to calculate percentiles for
        inverted_columns: List of columns where lower is better
        
    Returns:
        DataFrame with percentile columns added
    """
    inverted_columns = inverted_columns or []
    result = df.copy()
    
    for col in columns:
        if col in df.columns:
            invert = col in inverted_columns
            percentile_col = f"{col}_percentile"
            result[percentile_col] = calculate_percentiles(
                df[col].fillna(0),  # Handle NaN values
                invert=invert
            )
    
    return result


# Metric configurations for each stat type
BATTING_ADV_METRICS = [
    "pa", "bb_rate", "k_rate", "bb_per_k", "avg", "obp", "slg", 
    "ops", "iso", "spd", "babip", "wsb", "wrc", "wraa", "woba", "wrc_plus"
]

BATTING_ADV_INVERTED = ["k_rate"]

BATTING_STD_METRICS = [
    "g", "ab", "pa", "h", "single", "double", "triple", "hr", 
    "r", "rbi", "bb", "ibb", "so", "hbp", "sf", "sh", "gdp", "sb", "cs", "avg"
]

BATTING_STD_INVERTED = ["so", "gdp", "cs"]

PITCHING_ADV_METRICS = [
    "w", "l", "sv", "g", "gs", "ip", "k_per_9", "bb_per_9", 
    "hr_per_9", "babip", "lob_pct", "gb_pct", "hr_per_fb", 
    "era", "fip", "xfip", "siera"
]

PITCHING_ADV_INVERTED = [
    "l", "bb_per_9", "hr_per_9", "babip", "hr_per_fb", "era", "fip", "xfip", "siera"
]

PITCHING_STD_METRICS = [
    "w", "l", "era", "g", "gs", "cg", "sho", "sv", "ip", 
    "h", "r", "er", "hr", "bb", "ibb", "hbp", "wp", "bk", "so"
]

PITCHING_STD_INVERTED = [
    "l", "era", "h", "r", "er", "hr", "bb", "ibb", "hbp", "wp", "bk"
]


def process_batting_percentiles(
    df: pd.DataFrame,
    is_advanced: bool = True,
) -> pd.DataFrame:
    """
    Process batting data and calculate percentiles.
    
    Args:
        df: DataFrame with raw batting statistics
        is_advanced: Whether to use advanced or standard metrics
        
    Returns:
        DataFrame with percentile columns
    """
    if is_advanced:
        return calculate_all_percentiles(df, BATTING_ADV_METRICS, BATTING_ADV_INVERTED)
    else:
        return calculate_all_percentiles(df, BATTING_STD_METRICS, BATTING_STD_INVERTED)


def process_pitching_percentiles(
    df: pd.DataFrame,
    is_advanced: bool = True,
) -> pd.DataFrame:
    """
    Process pitching data and calculate percentiles.
    
    Args:
        df: DataFrame with raw pitching statistics
        is_advanced: Whether to use advanced or standard metrics
        
    Returns:
        DataFrame with percentile columns
    """
    if is_advanced:
        return calculate_all_percentiles(df, PITCHING_ADV_METRICS, PITCHING_ADV_INVERTED)
    else:
        return calculate_all_percentiles(df, PITCHING_STD_METRICS, PITCHING_STD_INVERTED)
