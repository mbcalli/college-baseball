# API Reference

## Overview

This document provides a comprehensive reference for all functions, database schemas, and configuration files in the college baseball statistics project.

## Python Modules

### `app.py`

Main application entry point for Streamlit.

#### Functions

**`main()`** (implicit)
- **Description**: Entry point that sets up navigation and launches app
- **Parameters**: None
- **Returns**: None
- **Side Effects**: Starts Streamlit server

#### Global Variables

- `pages` (List[st.Page]): List of application pages

---

### `helper.py`

Utility functions for data processing and visualization.

#### Color Functions

##### `perc_to_color(value: float) -> str`

Converts percentile to hex color on blue-to-red gradient.

**Parameters**:
- `value` (float): Percentile value (0-100)

**Returns**:
- `str`: Hex color code (e.g., "#FF0000")

**Example**:
```python
color = perc_to_color(75)  # Returns '#BF0040'
```

---

##### `perc_to_pastel_color(value: float, desaturation: float = 0.1) -> str`

Converts percentile to pastel version of blue-to-red gradient.

**Parameters**:
- `value` (float): Percentile value (0-100)
- `desaturation` (float, optional): Blend factor with white (default: 0.1)

**Returns**:
- `str`: Hex color code

**Example**:
```python
color = perc_to_pastel_color(50, desaturation=0.2)  # Lighter purple
```

---

#### Formatting Functions

##### `value_to_string(value: float) -> str`

Formats numeric value with appropriate precision.

**Parameters**:
- `value` (float): Numeric value to format

**Returns**:
- `str`: Formatted string

**Rules**:
- `value > 10`: No decimals (e.g., "245")
- `5 < value ≤ 10`: One decimal (e.g., "7.5")
- `1 < value ≤ 5`: Two decimals (e.g., "3.45")
- `value ≤ 1`: Three decimals (e.g., "0.287")

**Example**:
```python
formatted = value_to_string(0.287)  # Returns "0.287"
```

---

#### Data Preparation Functions - Batting

##### `get_adv_batter_df(player_name: str, silver_adv_batting: pd.DataFrame, bronze_adv_batting: pd.DataFrame) -> pd.DataFrame`

Prepares advanced batting statistics for single player visualization.

**Parameters**:
- `player_name` (str): Player's full name
- `silver_adv_batting` (pd.DataFrame): Silver table with percentiles
- `bronze_adv_batting` (pd.DataFrame): Bronze table with raw values

**Returns**:
- `pd.DataFrame`: DataFrame with columns:
  - `stat` (str): Stat abbreviation (e.g., "AVG")
  - `perc` (int): Percentile value (0-100)
  - `value` (float): Raw statistic value
  - `color` (str): Hex color code
  - `value_str` (str): Formatted value string

**Example**:
```python
import pandas as pd
import sqlite3

conn = sqlite3.connect("baseball.db")
silver = pd.read_sql("SELECT * FROM silver_adv_batting WHERE name = 'John Smith'", conn)
bronze = pd.read_sql("SELECT * FROM bronze_adv_batting WHERE name = 'John Smith'", conn)
conn.close()

df = get_adv_batter_df("John Smith", silver, bronze)
print(df.head())
```

---

##### `get_std_batter_df(player_name: str, silver_std_batting: pd.DataFrame, bronze_std_batting: pd.DataFrame) -> pd.DataFrame`

Prepares standard batting statistics for single player visualization.

**Parameters**: Same as `get_adv_batter_df()` but for standard stats

**Returns**: Same structure as `get_adv_batter_df()`

---

##### `get_team_stat_batting_df(team: str, stat: str, stat_fmt: str, min_pa: int = None) -> pd.DataFrame`

Prepares team batting comparison for single statistic.

**Parameters**:
- `team` (str): Team abbreviation (e.g., "CLEM")
- `stat` (str): Database column name (e.g., "avg")
- `stat_fmt` (str): Display name (e.g., "AVG")
- `min_pa` (int, optional): Minimum plate appearances filter

**Returns**:
- `pd.DataFrame`: DataFrame with columns:
  - `name` (str): Player name
  - `perc` (int): Percentile value
  - `value` (float): Raw value
  - `color` (str): Color code
  - `value_str` (str): Formatted value

**Example**:
```python
df = get_team_stat_batting_df("CLEM", "avg", "AVG", min_pa=100)
print(df.sort_values('perc', ascending=False))
```

---

#### Data Preparation Functions - Pitching

##### `get_adv_pitcher_df(player_name: str, silver_adv_pitching: pd.DataFrame, bronze_adv_pitching: pd.DataFrame) -> pd.DataFrame`

Prepares advanced pitching statistics for single player.

**Parameters**: Same pattern as batting functions

**Returns**: DataFrame with pitching stats (ERA, FIP, etc.)

---

##### `get_std_pitcher_df(player_name: str, silver_std_pitching: pd.DataFrame, bronze_std_pitching: pd.DataFrame) -> pd.DataFrame`

Prepares standard pitching statistics for single player.

---

##### `get_team_stat_pitching_df(team: str, stat: str, stat_fmt: str, min_ip: int = None) -> pd.DataFrame`

Prepares team pitching comparison for single statistic.

**Parameters**:
- `team` (str): Team abbreviation
- `stat` (str): Database column name
- `stat_fmt` (str): Display name
- `min_ip` (int, optional): Minimum innings pitched filter

---

#### Visualization Functions

##### `get_player_batting_figure(player_name: str, silver_table: pd.DataFrame, bronze_table: pd.DataFrame, is_advanced: bool) -> go.Figure`

Creates horizontal bar chart for individual batter.

**Parameters**:
- `player_name` (str): Player's name for title
- `silver_table` (pd.DataFrame): Silver data (advanced or standard)
- `bronze_table` (pd.DataFrame): Bronze data (advanced or standard)
- `is_advanced` (bool): True for advanced stats, False for standard

**Returns**:
- `plotly.graph_objects.Figure`: Configured Plotly figure

**Chart Features**:
- Horizontal bars
- Color gradient by percentile
- Percentile value inside bars
- Raw value annotations
- Static rendering

**Example**:
```python
fig = get_player_batting_figure("John Smith", silver, bronze, is_advanced=True)
st.plotly_chart(fig, config={"staticPlot": True})
```

---

##### `get_player_pitching_figure(player_name: str, silver_table: pd.DataFrame, bronze_table: pd.DataFrame, is_advanced: bool) -> go.Figure`

Creates horizontal bar chart for individual pitcher.

**Parameters**: Same as `get_player_batting_figure()`

**Returns**: Plotly figure with pitching stats

---

##### `get_team_stat_batting_fig(team: str, stat: str, stat_fmt: str, min_pa: int = None) -> go.Figure`

Creates team lineup comparison chart.

**Parameters**:
- `team` (str): Team abbreviation
- `stat` (str): Database column name
- `stat_fmt` (str): Display name for axis label
- `min_pa` (int, optional): Minimum PA filter

**Returns**:
- `plotly.graph_objects.Figure`: Team comparison chart

**Example**:
```python
fig = get_team_stat_batting_fig("CLEM", "avg", "AVG", min_pa=100)
st.plotly_chart(fig, config={"staticPlot": True})
```

---

##### `get_team_stat_pitching_fig(team: str, stat: str, stat_fmt: str, min_ip: int = None) -> go.Figure`

Creates team bullpen comparison chart.

**Parameters**: Same pattern as batting, uses min_ip

**Returns**: Plotly figure

---

## Database Schemas

### Bronze Tables

#### `bronze_adv_batting`

Advanced batting statistics (raw data).

**Columns**:
- `name` (TEXT): Player name
- `team` (TEXT): Team abbreviation
- `age` (INT): Player age
- `pa` (INT): Plate appearances
- `bb_rate` (REAL): Walk rate (%)
- `k_rate` (REAL): Strikeout rate (%)
- `bb_per_k` (REAL): Walks per strikeout
- `avg` (REAL): Batting average
- `obp` (REAL): On-base percentage
- `slg` (REAL): Slugging percentage
- `ops` (REAL): OBP + SLG
- `iso` (REAL): Isolated power
- `spd` (REAL): Speed score
- `babip` (REAL): BABIP
- `wsb` (REAL): Weighted stolen bases
- `wrc` (REAL): Weighted runs created
- `wraa` (REAL): Weighted runs above average
- `woba` (REAL): Weighted on-base average
- `wrc_plus` (REAL): wRC+ (100 = average)
- `alt_name` (TEXT): Alternative name
- `id` (TEXT, PRIMARY KEY): Fangraphs player ID

#### `bronze_std_batting`

Standard batting statistics (raw data).

**Columns**:
- `name`, `team`, `age`, `id` (same as advanced)
- `g` (INT): Games played
- `ab` (INT): At bats
- `pa` (INT): Plate appearances
- `h` (INT): Hits
- `single`, `double`, `triple`, `hr` (INT): Hit types
- `r` (INT): Runs scored
- `rbi` (INT): Runs batted in
- `bb`, `ibb` (INT): Walks, intentional walks
- `so` (INT): Strikeouts
- `hbp` (INT): Hit by pitch
- `sf`, `sh` (INT): Sacrifice flies, sacrifice hits
- `gdp` (INT): Grounded into double play
- `sb`, `cs` (INT): Stolen bases, caught stealing
- `avg` (REAL): Batting average

#### `bronze_adv_pitching`

Advanced pitching statistics (raw data).

**Columns**:
- `name`, `team`, `age`, `id` (same as batting)
- `w`, `l`, `sv` (INT): Wins, losses, saves
- `g`, `gs` (INT): Games, games started
- `ip` (REAL): Innings pitched
- `k_per_9`, `bb_per_9`, `hr_per_9` (REAL): Rate stats
- `babip` (REAL): BABIP against
- `lob_pct` (REAL): Left on base %
- `gb_pct` (REAL): Ground ball %
- `hr_per_fb` (REAL): HR per fly ball
- `era`, `fip`, `xfip`, `siera` (REAL): ERA metrics

#### `bronze_std_pitching`

Standard pitching statistics (raw data).

**Columns**:
- `name`, `team`, `age`, `id`
- `w`, `l` (INT): Wins, losses
- `era` (REAL): Earned run average
- `g`, `gs`, `cg`, `sho`, `sv` (INT): Game stats
- `ip` (REAL): Innings pitched
- `h`, `r`, `er`, `hr` (INT): Hits/runs allowed
- `bb`, `ibb`, `hbp` (INT): Walks, HBP
- `wp`, `bk` (INT): Wild pitches, balks
- `so` (INT): Strikeouts

### Silver Tables

All silver tables have the same structure: player identifiers plus percentile columns.

#### `silver_adv_batting`

**Columns**:
- `id` (TEXT, PRIMARY KEY): Player ID
- `name` (TEXT): Player name
- `team` (TEXT): Team abbreviation
- `{stat}_percentile` (INT): Percentile for each stat (0-100)

**Percentile Columns**: `pa_percentile`, `bb_rate_percentile`, `k_rate_percentile`, `bb_per_k_percentile`, `avg_percentile`, `obp_percentile`, `slg_percentile`, `ops_percentile`, `iso_percentile`, `spd_percentile`, `babip_percentile`, `wsb_percentile`, `wrc_percentile`, `wraa_percentile`, `woba_percentile`, `wrc_plus_percentile`

#### `silver_std_batting`

**Columns**: Same structure as advanced, with percentiles for standard stats

#### `silver_adv_pitching`

**Columns**: Same structure, with percentiles for advanced pitching stats

#### `silver_std_pitching`

**Columns**: Same structure, with percentiles for standard pitching stats

---

## Static Configuration Files

### `static/batters.json`

Maps teams to batter names for UI dropdowns.

**Format**:
```json
{
  "TEAM1": ["Player A", "Player B", ...],
  "TEAM2": ["Player C", "Player D", ...],
  ...
}
```

**Example**:
```json
{
  "CLEM": ["John Smith", "Jane Doe"],
  "UNC": ["Bob Johnson", "Alice Williams"]
}
```

### `static/pitchers.json`

Maps teams to pitcher names.

**Format**: Same as `batters.json`

### `static/batting_adv_metrics.json`

Descriptions of advanced batting metrics.

**Format**:
```json
{
  "STAT": "Description",
  ...
}
```

**Example**:
```json
{
  "PA": "Plate appearances",
  "BB%": "Walk rate (BB/PA)",
  "wRC+": "League-adjusted wRC (100 = average)"
}
```

### `static/batting_std_metrics.json`

Descriptions of standard batting metrics.

### `static/pitching_adv_metrics.json`

Descriptions of advanced pitching metrics.

### `static/pitching_std_metrics.json`

Descriptions of standard pitching metrics.

### `static/batting_metrics_map.json`

Maps display names to database columns for batting.

**Format**:
```json
{
  "DISPLAY_NAME": "db_column_name",
  ...
}
```

**Example**:
```json
{
  "AVG": "avg",
  "OBP": "obp",
  "SLG": "slg"
}
```

### `static/pitching_metrics_map.json`

Maps display names to database columns for pitching.

---

## Page Modules

### `pages/home.py`

Landing page with project information.

**Streamlit Components**:
- `st.title()`: Page title
- `st.info()`: Navigation hint
- `st.markdown()`: Content sections

### `pages/batting_individual.py`

Individual batter analysis page.

**Streamlit Components**:
- `st.selectbox()`: Team and player selection
- `st.toggle()`: Advanced/standard stats switch
- `st.button()`: Trigger visualization
- `st.plotly_chart()`: Display chart
- `st.dataframe()`: Metric descriptions

**Workflow**:
1. Load team/player data from JSON
2. User selects team, player, stat type
3. Query database on button click
4. Generate and display visualization
5. Show metric descriptions

### `pages/pitching_individual.py`

Individual pitcher analysis page.

**Structure**: Same as `batting_individual.py` for pitchers

### `pages/batting_team.py`

Team lineup comparison page.

**Streamlit Components**:
- `st.selectbox()`: Team, stat, minimum PA
- `st.button()`: Trigger visualization
- `st.plotly_chart()`: Display chart

### `pages/pitching_team.py`

Team bullpen comparison page.

**Structure**: Same as `batting_team.py` for pitchers

---

## ETL Scripts

### Bronze Load Scripts

Located in `bronze/load/`

**Pattern**: All scripts follow same structure:
1. Connect to database
2. Read CSV file
3. Clean/rename columns
4. Write to SQLite table
5. Close connection

**Scripts**:
- `load_adv_batting.py`
- `load_std_batting.py`
- `load_adv_pitching.py`
- `load_std_pitching.py`

### Silver Process Scripts

Located in `silver/process/`

**Pattern**: All scripts follow same structure:
1. Connect to database
2. Read bronze table
3. Calculate percentiles for each stat
4. Handle inverted metrics
5. Write to silver table
6. Close connection

**Scripts**:
- `process_adv_batting.py`
- `process_std_batting.py`
- `process_adv_pitching.py`
- `process_std_pitching.py`

### Table Creation Scripts

**`bronze/tables/create_bronze_tables.py`**:
- Reads SQL files from `bronze/tables/*.sql`
- Executes DDL to create bronze tables

**`silver/tables/create_silver_tables.py`**:
- Reads SQL files from `silver/tables/*.sql`
- Executes DDL to create silver tables

---

## Dependencies

From `requirements.txt`:

- `pandas>2.2.0`: Data manipulation
- `matplotlib==3.9.2`: Plotting (legacy)
- `numpy==1.26.4`: Numerical operations
- `scikit-learn==1.5.2`: Machine learning (percentiles)
- `pydantic==2.9.2`: Data validation
- `seaborn>=0.13.2`: Statistical plotting
- `plotly`: Interactive charts
- `streamlit`: Web application framework
- `sqlite3`: Database (built-in)

---

## Constants

### Inverted Metrics

**Batting**:
- Advanced: `k_rate`
- Standard: `so`, `gdp`, `cs`

**Pitching**:
- Advanced: `bb_per_9`, `hr_per_9`, `babip`, `hr_per_fb`, `era`, `fip`, `xfip`, `siera`
- Standard: `l`, `era`, `h`, `r`, `er`, `hr`, `bb`, `ibb`, `hbp`, `wp`, `bk`

### Color Palette

- Low percentile (0): `#0000FF` (blue)
- Mid percentile (50): `#800080` (purple)
- High percentile (100): `#FF0000` (red)
- Pastel adjustment: 10% blend with white by default
