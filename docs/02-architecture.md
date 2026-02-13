# Architecture

## System Design

The project follows a **medallion architecture** pattern (Bronze → Silver → Gold) commonly used in data engineering, adapted for this baseball analytics application.

## Architecture Diagram

```
┌─────────────────┐
│  Fangraphs CSV  │
│   (Raw Data)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         BRONZE LAYER                │
│  - Raw data ingestion               │
│  - CSV → SQLite tables              │
│  - Minimal transformations          │
│  - Tables: bronze_adv_batting,      │
│            bronze_adv_pitching,     │
│            bronze_std_batting,      │
│            bronze_std_pitching      │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         SILVER LAYER                │
│  - Data processing & enrichment     │
│  - Percentile calculations          │
│  - Normalized metrics               │
│  - Tables: silver_adv_batting,      │
│            silver_adv_pitching,     │
│            silver_std_batting,      │
│            silver_std_pitching      │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│       PRESENTATION LAYER            │
│  - Streamlit web application        │
│  - Interactive visualizations       │
│  - User filters & selections        │
│  - Pages: Home, Individual Batting, │
│           Individual Pitching,      │
│           Team Lineup, Team Bullpen │
└─────────────────────────────────────┘
```

## Layer Responsibilities

### Bronze Layer (`bronze/`)

**Purpose**: Store raw data with minimal processing

**Components**:
- `data/`: CSV files downloaded from Fangraphs
- `tables/`: SQL schema definitions for bronze tables
- `load/`: Python scripts to load CSVs into SQLite

**Characteristics**:
- Data stored as-is from source
- Simple column renaming for consistency
- Primary key management
- No business logic or calculations

### Silver Layer (`silver/`)

**Purpose**: Transform and enrich data for analysis

**Components**:
- `tables/`: SQL schema definitions for silver tables
- `process/`: Python scripts for percentile calculations

**Characteristics**:
- Percentile rankings calculated for all metrics
- Inverted metrics handled (lower is better)
- Results stored as integers (0-100)
- References bronze layer as source

### Presentation Layer (`pages/`, `app.py`, `helper.py`)

**Purpose**: Deliver interactive user experience

**Components**:
- `app.py`: Main application entry point with page navigation
- `pages/`: Individual page modules for different views
- `helper.py`: Shared visualization and data manipulation functions
- `static/`: JSON configuration files for metrics and players

**Characteristics**:
- Reads from silver and bronze layers
- Creates dynamic Plotly visualizations
- Handles user input and filtering
- No data transformation logic

## Data Flow

1. **Data Acquisition**: Download CSVs from Fangraphs
2. **Bronze Load**: Run `load_*.py` scripts to populate bronze tables
3. **Silver Process**: Run `process_*.py` scripts to calculate percentiles
4. **Application Access**: Streamlit app queries silver (percentiles) and bronze (raw values)
5. **Visualization**: Helper functions merge data and create charts

## Database Schema

The application uses a single SQLite database (`baseball.db`) with 8 tables:

### Bronze Tables
- `bronze_adv_batting`: Advanced batting stats (wRC+, wOBA, etc.)
- `bronze_std_batting`: Standard batting stats (H, HR, RBI, etc.)
- `bronze_adv_pitching`: Advanced pitching stats (FIP, SIERA, etc.)
- `bronze_std_pitching`: Standard pitching stats (W, ERA, K, etc.)

### Silver Tables
- `silver_adv_batting`: Percentiles for advanced batting
- `silver_std_batting`: Percentiles for standard batting
- `silver_adv_pitching`: Percentiles for advanced pitching
- `silver_std_pitching`: Percentiles for standard pitching

## Technology Choices

### Why SQLite?
- Lightweight, serverless database
- Perfect for single-user, local deployment
- No infrastructure required
- Easy to backup and version control

### Why Streamlit?
- Rapid prototyping of data applications
- Built-in UI components
- Python-native (no HTML/CSS/JavaScript required)
- Great for internal tools and dashboards

### Why Plotly?
- Interactive charts out of the box
- Extensive customization options
- Works seamlessly with Streamlit
- Professional-looking visualizations

### Why Pandas?
- Industry standard for data manipulation
- Excellent SQLite integration
- Rich statistical functions
- Easy percentile calculations

## File Organization

```
college-baseball/
├── app.py                 # Main entry point
├── helper.py              # Shared functions
├── baseball.db            # SQLite database
├── bronze/                # Bronze layer
│   ├── data/             # Raw CSV files
│   ├── load/             # ETL scripts
│   └── tables/           # Schema definitions
├── silver/                # Silver layer
│   ├── process/          # Percentile calculations
│   └── tables/           # Schema definitions
├── pages/                 # Streamlit pages
├── static/                # Configuration JSON files
└── docs/                  # Documentation
```

## Scalability Considerations

**Current State**: Designed for single-user, local analysis

**Future Enhancements**:
- Migrate to PostgreSQL for multi-user access
- Add automated data pipeline from Fangraphs API (if available)
- Implement caching for frequently accessed queries
- Add user authentication for team-specific views
- Deploy to cloud platform (Streamlit Cloud, AWS, etc.)
