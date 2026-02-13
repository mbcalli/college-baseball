# College Baseball Statistics Documentation

Welcome to the College Baseball Statistics project documentation. This project provides an interactive web application for visualizing and analyzing college baseball statistics using percentile-based metrics.

## Table of Contents

1. [Project Overview](./01-project-overview.md)
2. [Architecture](./02-architecture.md)
3. [Data Pipeline](./03-data-pipeline.md)
4. [Bronze Layer](./04-bronze-layer.md)
5. [Silver Layer](./05-silver-layer.md)
6. [Frontend Application](./06-frontend-application.md)
7. [Helper Functions](./07-helper-functions.md)
8. [Setup & Installation](./08-setup-installation.md)
9. [Data Update Guide](./09-data-update-guide.md)
10. [API Reference](./10-api-reference.md)

## Quick Links

- **Main Application**: `app.py`
- **Configuration**: `requirements.txt`
- **Data Sources**: `bronze/data/`
- **Database**: `baseball.db` (SQLite)

## Project Status

Last updated: 8 months ago (June 2025)  
Current season: 2025 data  
Next update needed: Before 2026 season

## Key Features

- **Individual Player Analysis**: View percentile-based statistics for individual batters and pitchers
- **Team Analysis**: Compare entire team lineups and bullpens
- **Standard & Advanced Metrics**: Toggle between standard baseball stats and advanced sabermetrics
- **Interactive Visualizations**: Plotly-based charts with percentile rankings
- **Minimum Playing Time Filters**: Filter players by minimum plate appearances or innings pitched

## Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy, scikit-learn
- **Database**: SQLite
- **Language**: Python 3.x

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Data Source

Data is sourced from [Fangraphs College Leaderboard](https://www.fangraphs.com/leaders/college) (requires membership for access).
