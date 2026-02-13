# Data Pipeline

## Overview

The data pipeline transforms raw CSV files from Fangraphs into an interactive web application. The process follows a clear sequence: **Acquire → Load → Process → Present**.

## Pipeline Stages

### 1. Data Acquisition

**Source**: [Fangraphs College Leaderboard](https://www.fangraphs.com/leaders/college)

**Requirements**: Fangraphs membership for data export

**Process**:
1. Navigate to Fangraphs College Leaderboard
2. Select desired season (e.g., 2025)
3. Choose stat type (Standard or Advanced)
4. Choose player type (Batting or Pitching)
5. Export data as CSV
6. Save to appropriate location in `bronze/data/`

**Expected Files**:
- `bronze/data/adv_batting.csv`
- `bronze/data/std_batting.csv`
- `bronze/data/adv_pitching.csv`
- `bronze/data/std_pitching.csv`

### 2. Database Initialization

**Purpose**: Create empty tables in SQLite database

**Script**: `bronze/tables/create_bronze_tables.py`

```bash
python bronze/tables/create_bronze_tables.py
```

**Actions**:
- Creates `baseball.db` if it doesn't exist
- Executes SQL scripts to create bronze tables
- Creates silver tables (via similar script in `silver/tables/`)

**Output**:
```
Table 'bronze_adv_batting' created in 'baseball.db'
Table 'bronze_adv_pitching' created in 'baseball.db'
Table 'bronze_std_batting' created in 'baseball.db'
Table 'bronze_std_pitching' created in 'baseball.db'
```

### 3. Bronze Layer Load

**Purpose**: Load raw CSV data into bronze tables

**Scripts** (run in order):
```bash
python bronze/load/load_adv_batting.py
python bronze/load/load_std_batting.py
python bronze/load/load_adv_pitching.py
python bronze/load/load_std_pitching.py
```

**Process for each script**:
1. Read CSV file using pandas
2. Clean data (remove null columns, rename columns)
3. Write to SQLite table using `to_sql(if_exists="replace")`
4. Print confirmation with record count

**Example Output**:
```
Table 'bronze_adv_batting' replaced with new data. 1247 records added.
```

**Key Transformations**:
- Remove `MLBAMID` column (always null)
- Rename columns to match database schema (lowercase, underscores)
- Preserve all raw values unchanged

### 4. Silver Layer Processing

**Purpose**: Calculate percentile rankings for all statistics

**Scripts** (run in order):
```bash
python silver/process/process_adv_batting.py
python silver/process/process_std_batting.py
python silver/process/process_adv_pitching.py
python silver/process/process_std_pitching.py
```

**Process for each script**:
1. Read data from corresponding bronze table
2. Identify columns to percentile-rank
3. For each column:
   - Calculate percentile using `pandas.rank(pct=True)`
   - Multiply by 100 for 0-100 scale
   - Invert if "lower is better" (e.g., K% for batters)
   - Convert to integer
4. Write to silver table with percentiles only
5. Print confirmation

**Example Output**:
```
Table 'silver_adv_batting' replaced with new data. 1247 records added.
```

**Percentile Calculation**:
```python
# Standard metric (higher is better)
data[percentile_column] = data[column].rank(pct=True) * 100

# Inverted metric (lower is better, e.g., K%)
data[percentile_column] = (-1 * data[column]).rank(pct=True) * 100
```

### 5. Static Asset Generation

**Purpose**: Create JSON files for UI dropdowns and metric descriptions

**Files to Update**:
- `static/batters.json`: Team → [Player names]
- `static/pitchers.json`: Team → [Player names]
- `static/batting_adv_metrics.json`: Metric definitions
- `static/batting_std_metrics.json`: Metric definitions
- `static/pitching_adv_metrics.json`: Metric definitions
- `static/pitching_std_metrics.json`: Metric definitions
- `static/batting_metrics_map.json`: UI display name → DB column
- `static/pitching_metrics_map.json`: UI display name → DB column

**Note**: These files may need manual updates when new seasons are added or rosters change.

### 6. Application Launch

**Command**:
```bash
streamlit run app.py
```

**Access**: Opens browser to `http://localhost:8501`

## Complete Pipeline Execution

For a full data refresh:

```bash
# 1. Place new CSV files in bronze/data/

# 2. Create tables (if first time or schema changed)
python bronze/tables/create_bronze_tables.py
python silver/tables/create_silver_tables.py

# 3. Load bronze layer
python bronze/load/load_adv_batting.py
python bronze/load/load_std_batting.py
python bronze/load/load_adv_pitching.py
python bronze/load/load_std_pitching.py

# 4. Process silver layer
python silver/process/process_adv_batting.py
python silver/process/process_std_batting.py
python silver/process/process_adv_pitching.py
python silver/process/process_std_pitching.py

# 5. Update static JSON files (manual)

# 6. Launch application
streamlit run app.py
```

## Pipeline Best Practices

### Error Handling
- Always check record counts after loading
- Verify all CSV files are present before starting
- Backup `baseball.db` before re-running loads

### Data Validation
- Compare row counts between bronze and silver layers
- Spot-check percentiles (50th percentile should be near median)
- Verify inverted metrics are correct (high K% → low percentile for batters)

### Performance
- Bronze and silver loads are fast (<5 seconds each)
- Percentile calculations scale linearly with player count
- No indexes needed for current data volume

### Troubleshooting

**Issue**: CSV column names don't match expectations
- **Solution**: Update column mappings in load scripts

**Issue**: Percentiles seem wrong
- **Solution**: Check `lower_is_better` list in process scripts

**Issue**: Players missing from dropdowns
- **Solution**: Regenerate `batters.json` and `pitchers.json` from bronze tables

**Issue**: Database locked error
- **Solution**: Close any open SQLite connections or applications

## Data Refresh Frequency

**Recommended**: 
- Weekly during season
- Daily during playoffs or critical periods
- At minimum, refresh before each season starts

**Time Required**: ~2 minutes for complete pipeline execution
