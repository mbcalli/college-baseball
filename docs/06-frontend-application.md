# Frontend Application

## Overview

The frontend is built with **Streamlit**, a Python framework for creating data applications. It provides an interactive web interface for exploring baseball statistics.

## Application Structure

```
app.py                          # Main entry point
helper.py                       # Shared visualization functions
pages/
├── home.py                     # Landing page
├── batting_individual.py       # Individual batter analysis
├── batting_team.py             # Team lineup comparison
├── pitching_individual.py      # Individual pitcher analysis
└── pitching_team.py            # Team bullpen comparison
static/
├── batters.json                # Team → batters mapping
├── pitchers.json               # Team → pitchers mapping
├── batting_adv_metrics.json    # Advanced batting metric descriptions
├── batting_std_metrics.json    # Standard batting metric descriptions
├── pitching_adv_metrics.json   # Advanced pitching metric descriptions
├── pitching_std_metrics.json   # Standard pitching metric descriptions
├── batting_metrics_map.json    # Display name → database column mapping
└── pitching_metrics_map.json   # Display name → database column mapping
```

## Main Application (`app.py`)

```python
import streamlit as st

pages = [
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/batting_individual.py", title="Individual Batting"),
    st.Page("pages/pitching_individual.py", title="Individual Pitching"),
    st.Page("pages/batting_team.py", title="Team Lineup"),
    st.Page("pages/pitching_team.py", title="Team Bullpen"),
]

pg = st.navigation(pages)
pg.run()
```

**Purpose**: 
- Define navigation structure
- Register all pages
- Launch Streamlit server

**Running**:
```bash
streamlit run app.py
```

**Access**: `http://localhost:8501`

## Pages

### Home Page (`pages/home.py`)

**Purpose**: Welcome page with project overview and usage instructions

**Content**:
- Title and navigation instructions
- Explanation of percentiles
- Motivation for the project
- Data source attribution

**Key Sections**:
1. **Percentiles Explanation**: How to interpret percentile rankings
2. **Inverted Metrics**: Why some stats are "better when lower"
3. **Playing Time Context**: Importance of minimum PA/IP filters
4. **Motivation**: Link to Baseball Savant inspiration
5. **Data Source**: Fangraphs attribution

### Individual Batting (`pages/batting_individual.py`)

**Purpose**: View percentile rankings for a single batter

**UI Components**:
1. **Team Selector**: Dropdown of all teams
2. **Player Selector**: Dropdown of batters on selected team
3. **Stats Toggle**: Switch between standard and advanced stats
4. **Show Button**: Generate visualization

**Workflow**:
```python
# 1. User selects team and player
team_name = st.selectbox("Team", list(batters.keys()))
batter_name = st.selectbox("Batter", batters[team_name])
use_advanced = st.toggle("Advanced Stats", value=True)

# 2. On button click, query database
if st.button("Show"):
    connection = sqlite3.connect("baseball.db")
    if use_advanced:
        bronze = pd.read_sql(f"SELECT * FROM bronze_adv_batting WHERE name = '{batter_name}'", connection)
        silver = pd.read_sql(f"SELECT * FROM silver_adv_batting WHERE name = '{batter_name}'", connection)
    else:
        # Similar for standard stats
    connection.close()

    # 3. Generate figure
    fig = get_player_batting_figure(batter_name, silver, bronze, use_advanced)
    st.plotly_chart(fig, config={"staticPlot": True})

    # 4. Show metric descriptions
    with open("static/batting_adv_metrics.json", "r") as file:
        metrics = json.load(file)
    df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Description"])
    st.dataframe(df, use_container_width=True, hide_index=True)
```

**Output**: Horizontal bar chart with percentile rankings

### Team Lineup (`pages/batting_team.py`)

**Purpose**: Compare all batters on a team for a specific statistic

**UI Components**:
1. **Team Selector**: Choose team
2. **Statistic Selector**: Choose which stat to compare (AVG, OPS, wRC+, etc.)
3. **Minimum PA Filter**: Set minimum plate appearances (0, 50, 100, 150, 200)
4. **Show Button**: Generate visualization

**Workflow**:
```python
# 1. User selections
team_name = st.selectbox("Team", list(batters.keys()))
stat_name = st.selectbox("Statistic", list(batting_metrics.keys()))
min_pa = st.selectbox("Minimum PA", options=[0, 50, 100, 150, 200])

# 2. Generate team comparison
if st.button("Show"):
    fig = get_team_stat_batting_fig(team_name, batting_metrics[stat_name], stat_name, min_pa=min_pa)
    st.plotly_chart(fig, config={"staticPlot": True})
```

**Output**: Horizontal bar chart comparing all qualified players on team

### Individual Pitching (`pages/pitching_individual.py`)

**Purpose**: View percentile rankings for a single pitcher

**Structure**: Nearly identical to `batting_individual.py`, but for pitchers

**Key Differences**:
- Uses `pitchers.json` instead of `batters.json`
- Queries pitching tables instead of batting tables
- Uses `get_player_pitching_figure()` instead of batting version

### Team Bullpen (`pages/pitching_team.py`)

**Purpose**: Compare all pitchers on a team for a specific statistic

**Structure**: Nearly identical to `batting_team.py`, but for pitchers

**Key Differences**:
- Uses minimum IP (innings pitched) instead of minimum PA
- Queries pitching tables instead of batting tables

## Static Configuration Files

### Player Mappings

**`static/batters.json`**:
```json
{
  "CLEM": ["Player One", "Player Two", ...],
  "UNC": ["Player A", "Player B", ...],
  ...
}
```

**`static/pitchers.json`**: Same structure for pitchers

**Usage**: Populate team and player dropdowns

### Metric Descriptions

**`static/batting_adv_metrics.json`**:
```json
{
  "PA": "Plate appearances",
  "BB%": "Walk rate (BB/PA)",
  "K%": "Strikeout rate (K/PA)",
  "wRC+": "League-adjusted wRC (100 = average)",
  ...
}
```

**Usage**: Display table explaining each metric

### Metric Mappings

**`static/batting_metrics_map.json`**:
```json
{
  "AVG": "avg",
  "OBP": "obp",
  "SLG": "slg",
  "OPS": "ops",
  ...
}
```

**Purpose**: Map user-friendly display names to database column names

## Streamlit Configuration

### Layout

The app uses Streamlit's default layout with:
- **Wide mode**: Disabled (uses centered column)
- **Sidebar**: Navigation menu (automatic with `st.navigation()`)
- **Theme**: Default Streamlit theme

### Custom Configuration

To customize, create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
```

## User Interaction Flow

### Typical Session

1. **Launch Application**: User runs `streamlit run app.py`
2. **Home Page**: Read overview and instructions
3. **Navigate**: Use sidebar to select page
4. **Make Selections**: Choose team, player, stat, filters
5. **View Results**: Click "Show" to generate visualization
6. **Interpret**: Read percentiles and metric descriptions
7. **Repeat**: Explore different players/teams/stats

### Navigation

- **Sidebar Menu**: Click ▶️ in top-left to open navigation
- **Page Selection**: Click page name to switch views
- **Persistent State**: Streamlit maintains selections within a page

## Visualization Types

### Individual Player Chart

**Type**: Horizontal bar chart with annotations

**Features**:
- Bars colored by percentile (gradient from blue → purple → red)
- Percentile value displayed inside each bar
- Raw statistic value displayed at end of bar
- Metrics sorted by type (descriptive at top, performance at bottom)
- Static plot (no zoom/pan for cleaner presentation)

### Team Comparison Chart

**Type**: Horizontal bar chart with player names

**Features**:
- Each bar represents one player
- Bars colored by percentile
- Raw values and percentiles displayed
- Filtered by minimum playing time
- Sorted by percentile (best at top)

## State Management

Streamlit uses a run-from-top model where the entire script re-runs on each interaction. State is managed through:

1. **Widget Keys**: Unique identifiers for each input
   ```python
   st.selectbox("Team", options, key="batting_team_ind")
   ```

2. **Session State**: Persist values across reruns
   ```python
   if 'selected_player' not in st.session_state:
       st.session_state.selected_player = None
   ```

3. **Caching**: Cache expensive operations
   ```python
   @st.cache_data
   def load_player_data():
       # Expensive operation
       return data
   ```

## Performance Optimization

### Current Approach

- **No Caching**: Database queries are fast enough (<10ms)
- **Static Plots**: Disabled interactivity for faster rendering
- **Lazy Loading**: Data only fetched when "Show" is clicked

### Future Optimizations

If performance becomes an issue:

1. **Cache Database Connections**:
   ```python
   @st.cache_resource
   def get_connection():
       return sqlite3.connect("baseball.db")
   ```

2. **Cache Query Results**:
   ```python
   @st.cache_data
   def load_player_stats(player_name, stat_type):
       # Query database
       return data
   ```

3. **Preload Static Data**:
   ```python
   @st.cache_data
   def load_teams_and_players():
       with open("static/batters.json") as f:
           return json.load(f)
   ```

## Error Handling

### Current Implementation

- **Basic SQL Injection**: Uses f-strings (not production-safe)
- **Missing Files**: No error handling for missing JSON files
- **Invalid Selections**: Assumes valid data from dropdowns

### Recommended Improvements

```python
# Parameterized queries
cursor.execute("SELECT * FROM bronze_adv_batting WHERE name = ?", (player_name,))

# File existence checks
if not os.path.exists("static/batters.json"):
    st.error("Configuration file missing. Please contact administrator.")
    st.stop()

# Data validation
if len(silver) == 0:
    st.warning(f"No data found for {player_name}")
    st.stop()
```

## Accessibility

### Current State

Streamlit provides:
- Keyboard navigation
- Screen reader support (basic)
- Responsive design

### Limitations

- Color-blind friendly colors not enforced
- No alternative text for visualizations
- Limited ARIA labels

### Improvements

```python
# Add alt text to charts
fig.update_layout(
    title={
        'text': f"{player_name} - Batting Statistics",
        'aria-label': f"Horizontal bar chart showing percentile rankings for {player_name}"
    }
)

# Use color-blind friendly palette
colors = px.colors.qualitative.Safe  # Color-blind friendly
```

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Connect repository at share.streamlit.io
3. Deploy automatically

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### AWS/GCP/Azure
- Use container service (ECS, Cloud Run, App Service)
- Mount `baseball.db` as persistent volume
- Configure load balancer if needed
