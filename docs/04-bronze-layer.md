# Bronze Layer

## Purpose

The bronze layer stores raw, minimally processed data from Fangraphs. It serves as the single source of truth and maintains data lineage from source to analysis.

## Directory Structure

```
bronze/
├── data/                    # CSV files from Fangraphs
│   ├── adv_batting.csv
│   ├── adv_pitching.csv
│   ├── std_batting.csv
│   └── std_pitching.csv
├── load/                    # ETL scripts
│   ├── load_adv_batting.py
│   ├── load_adv_pitching.py
│   ├── load_std_batting.py
│   └── load_std_pitching.py
└── tables/                  # SQL schemas
    ├── create_bronze_tables.py
    ├── bronze_adv_batting.sql
    ├── bronze_adv_pitching.sql
    ├── bronze_std_batting.sql
    └── bronze_std_pitching.sql
```

## Data Files

### `bronze/data/adv_batting.csv`

**Source**: Fangraphs College Leaderboard → Advanced Batting

**Columns** (from Fangraphs):
- Name, Team, Age
- PA (Plate Appearances)
- BB% (Walk Rate)
- K% (Strikeout Rate)
- BB/K (Walks per Strikeout)
- AVG (Batting Average)
- OBP (On-Base Percentage)
- SLG (Slugging Percentage)
- OPS (On-Base Plus Slugging)
- ISO (Isolated Power)
- Spd (Speed Score)
- BABIP (Batting Average on Balls In Play)
- wSB (Weighted Stolen Bases)
- wRC (Weighted Runs Created)
- wRAA (Weighted Runs Above Average)
- wOBA (Weighted On-Base Average)
- wRC+ (Weighted Runs Created Plus)
- MLBAMID (always null, removed during load)
- alt_name (alternative name)
- playerid (Fangraphs ID)

### `bronze/data/std_batting.csv`

**Source**: Fangraphs College Leaderboard → Standard Batting

**Columns**:
- Name, Team, Age
- G (Games), AB (At Bats), PA (Plate Appearances)
- H (Hits), 1B, 2B, 3B, HR
- R (Runs), RBI
- BB (Walks), IBB (Intentional Walks), SO (Strikeouts)
- HBP (Hit By Pitch)
- SF (Sacrifice Flies), SH (Sacrifice Hits)
- GDP (Grounded into Double Play)
- SB (Stolen Bases), CS (Caught Stealing)
- AVG (Batting Average)
- alt_name, playerid

### `bronze/data/adv_pitching.csv`

**Source**: Fangraphs College Leaderboard → Advanced Pitching

**Columns**:
- Name, Team, Age
- W (Wins), L (Losses), SV (Saves)
- G (Games), GS (Games Started)
- IP (Innings Pitched)
- K/9 (Strikeouts per 9 innings)
- BB/9 (Walks per 9 innings)
- HR/9 (Home Runs per 9 innings)
- BABIP, LOB% (Left on Base Percentage)
- GB% (Ground Ball Percentage)
- HR/FB (Home Run to Fly Ball Ratio)
- ERA (Earned Run Average)
- FIP (Fielding Independent Pitching)
- xFIP (Expected FIP)
- SIERA (Skill-Interactive ERA)
- alt_name, playerid

### `bronze/data/std_pitching.csv`

**Source**: Fangraphs College Leaderboard → Standard Pitching

**Columns**:
- Name, Team, Age
- W, L, ERA, G, GS, CG (Complete Games), ShO (Shutouts), SV
- IP, H (Hits Allowed), R (Runs), ER (Earned Runs)
- HR (Home Runs Allowed)
- BB (Walks), IBB, HBP, WP (Wild Pitches), BK (Balks)
- SO (Strikeouts)
- alt_name, playerid

## Table Schemas

### `bronze_adv_batting`

```sql
CREATE TABLE IF NOT EXISTS bronze_adv_batting (
    name TEXT,
    team TEXT,
    age INT,
    pa INT,
    bb_rate REAL,
    k_rate REAL,
    bb_per_k REAL,
    avg REAL,
    obp REAL,
    slg REAL,
    ops REAL,
    iso REAL,
    spd REAL,
    babip REAL,
    wsb REAL,
    wrc REAL,
    wraa REAL,
    woba REAL,
    wrc_plus REAL,
    alt_name TEXT,
    id TEXT PRIMARY KEY
)
```

### `bronze_std_batting`

```sql
CREATE TABLE IF NOT EXISTS bronze_std_batting (
    name TEXT,
    team TEXT,
    age INT,
    g INT,
    ab INT,
    pa INT,
    h INT,
    single INT,
    double INT,
    triple INT,
    hr INT,
    r INT,
    rbi INT,
    bb INT,
    ibb INT,
    so INT,
    hbp INT,
    sf INT,
    sh INT,
    gdp INT,
    sb INT,
    cs INT,
    avg REAL,
    alt_name TEXT,
    id TEXT PRIMARY KEY
)
```

### `bronze_adv_pitching`

```sql
CREATE TABLE IF NOT EXISTS bronze_adv_pitching (
    name TEXT,
    team TEXT,
    age INT,
    w INT,
    l INT,
    sv INT,
    g INT,
    gs INT,
    ip REAL,
    k_per_9 REAL,
    bb_per_9 REAL,
    hr_per_9 REAL,
    babip REAL,
    lob_pct REAL,
    gb_pct REAL,
    hr_per_fb REAL,
    era REAL,
    fip REAL,
    xfip REAL,
    siera REAL,
    alt_name TEXT,
    id TEXT PRIMARY KEY
)
```

### `bronze_std_pitching`

```sql
CREATE TABLE IF NOT EXISTS bronze_std_pitching (
    name TEXT,
    team TEXT,
    age INT,
    w INT,
    l INT,
    era REAL,
    g INT,
    gs INT,
    cg INT,
    sho INT,
    sv INT,
    ip REAL,
    h INT,
    r INT,
    er INT,
    hr INT,
    bb INT,
    ibb INT,
    hbp INT,
    wp INT,
    bk INT,
    so INT,
    alt_name TEXT,
    id TEXT PRIMARY KEY
)
```

## Load Scripts

All load scripts follow the same pattern:

### Example: `load_adv_batting.py`

```python
import pandas as pd
import sqlite3

# Connect to database
connection = sqlite3.connect("baseball.db")
cursor = connection.cursor()

# Load CSV
data = pd.read_csv("bronze/data/adv_batting.csv")

# Clean data
data = data.drop(columns=["MLBAMID"])  # Always null

# Rename columns to match schema
data.columns = ["name", "team", "age", "pa", "bb_rate", 
                "k_rate", "bb_per_k", "avg", "obp", "slg", 
                "ops", "iso", "spd", "babip", "wsb", "wrc", 
                "wraa", "woba", "wrc_plus", "alt_name", "id"]

# Write to database (replace existing data)
data.to_sql("bronze_adv_batting", connection, 
            if_exists="replace", index=False)

connection.close()

print(f"Table 'bronze_adv_batting' replaced with new data. {len(data)} records added.")
```

## Key Design Decisions

### Why Store Raw Data?

1. **Data Lineage**: Always trace back to original source
2. **Reprocessing**: Recalculate percentiles without re-downloading
3. **Debugging**: Verify transformations against source
4. **Flexibility**: Add new metrics without changing source

### Why Use SQLite?

1. **Simplicity**: No server setup required
2. **Performance**: Fast enough for this data volume
3. **Portability**: Single file database
4. **Integration**: Native pandas support

### Column Naming Convention

- Lowercase with underscores (snake_case)
- Full words when possible (avoid abbreviations)
- Consistent across tables
- Match common baseball terminology

### Data Types

- **TEXT**: Names, teams, identifiers
- **INT**: Counting stats (games, hits, etc.)
- **REAL**: Rates and percentages (ERA, AVG, etc.)

### Primary Keys

- Use Fangraphs `playerid` as primary key
- Renamed to `id` for consistency
- Ensures unique player records
- Enables joins between tables

## Data Validation

After loading, verify:

```sql
-- Check record counts
SELECT COUNT(*) FROM bronze_adv_batting;
SELECT COUNT(*) FROM bronze_std_batting;
SELECT COUNT(*) FROM bronze_adv_pitching;
SELECT COUNT(*) FROM bronze_std_pitching;

-- Check for nulls in key columns
SELECT COUNT(*) FROM bronze_adv_batting WHERE name IS NULL;
SELECT COUNT(*) FROM bronze_adv_batting WHERE id IS NULL;

-- Check for duplicates
SELECT id, COUNT(*) FROM bronze_adv_batting GROUP BY id HAVING COUNT(*) > 1;

-- Spot check specific players
SELECT * FROM bronze_adv_batting WHERE name LIKE '%Smith%';
```

## Maintenance

### Adding New Season Data

1. Download new CSVs from Fangraphs
2. Replace files in `bronze/data/`
3. Run all load scripts
4. Verify record counts match Fangraphs
5. Proceed to silver layer processing

### Schema Changes

If Fangraphs adds/removes columns:

1. Update SQL schema in `bronze/tables/*.sql`
2. Update column mappings in `load_*.py` scripts
3. Drop and recreate tables
4. Run load scripts
5. Update downstream silver layer processing

### Performance Optimization

Current setup is sufficient for ~1,000-2,000 players per category. If performance becomes an issue:

- Add indexes on frequently queried columns (name, team)
- Use `PRAGMA` statements to optimize SQLite
- Consider batching inserts instead of `to_sql()`
