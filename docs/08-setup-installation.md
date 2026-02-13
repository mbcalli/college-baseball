# Setup & Installation

## Prerequisites

### System Requirements

- **Operating System**: macOS, Linux, or Windows
- **Python**: Version 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB for dependencies and database

### Required Software

1. **Python 3.8+**
   - Check version: `python --version` or `python3 --version`
   - Download: [python.org](https://www.python.org/downloads/)

2. **pip** (Python package manager)
   - Usually included with Python
   - Check version: `pip --version` or `pip3 --version`

3. **Git** (optional, for version control)
   - Check version: `git --version`
   - Download: [git-scm.com](https://git-scm.com/)

## Installation Steps

### 1. Clone or Download Repository

**Option A: Using Git**
```bash
git clone https://github.com/mbcalli/college-baseball.git
cd college-baseball
```

**Option B: Download ZIP**
1. Download repository as ZIP file
2. Extract to desired location
3. Navigate to directory in terminal

### 2. Create Virtual Environment (Recommended)

**Why?** Isolates project dependencies from system Python packages.

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**Verify Activation**: Your terminal prompt should show `(venv)` prefix.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output**:
```
Collecting pandas>2.2.0
Collecting matplotlib==3.9.2
...
Successfully installed pandas-2.2.2 matplotlib-3.9.2 ...
```

**Verify Installation**:
```bash
pip list
```

### 4. Verify Installation

```bash
python -c "import streamlit; print(streamlit.__version__)"
python -c "import pandas; print(pandas.__version__)"
python -c "import plotly; print(plotly.__version__)"
```

## Initial Data Setup

### Option 1: Use Existing Database (If Provided)

If `baseball.db` is included in the repository:

1. Verify file exists:
   ```bash
   ls -lh baseball.db
   ```

2. Test database:
   ```bash
   sqlite3 baseball.db "SELECT COUNT(*) FROM bronze_adv_batting;"
   ```

3. Skip to [Running the Application](#running-the-application)

### Option 2: Load Data from CSVs

If starting from scratch or updating data:

#### Step 1: Obtain CSV Files

1. Visit [Fangraphs College Leaderboard](https://www.fangraphs.com/leaders/college) (requires membership)
2. Download four CSV files:
   - Advanced Batting
   - Standard Batting
   - Advanced Pitching
   - Standard Pitching

3. Place files in `bronze/data/`:
   ```
   bronze/data/
   ├── adv_batting.csv
   ├── adv_pitching.csv
   ├── std_batting.csv
   └── std_pitching.csv
   ```

#### Step 2: Create Database Tables

```bash
# Create bronze tables
python bronze/tables/create_bronze_tables.py

# Create silver tables
python silver/tables/create_silver_tables.py
```

**Expected Output**:
```
Table 'bronze_adv_batting' created in 'baseball.db'
Table 'bronze_adv_pitching' created in 'baseball.db'
Table 'bronze_std_batting' created in 'baseball.db'
Table 'bronze_std_pitching' created in 'baseball.db'
```

#### Step 3: Load Bronze Layer

```bash
python bronze/load/load_adv_batting.py
python bronze/load/load_std_batting.py
python bronze/load/load_adv_pitching.py
python bronze/load/load_std_pitching.py
```

**Expected Output** (for each):
```
Table 'bronze_adv_batting' replaced with new data. 1247 records added.
```

#### Step 4: Process Silver Layer

```bash
python silver/process/process_adv_batting.py
python silver/process/process_std_batting.py
python silver/process/process_adv_pitching.py
python silver/process/process_std_pitching.py
```

**Expected Output** (for each):
```
Table 'silver_adv_batting' replaced with new data. 1247 records added.
```

#### Step 5: Update Static JSON Files

The `static/` directory contains configuration files that may need updating:

**`static/batters.json`** - Generate from database:
```python
import sqlite3
import json

conn = sqlite3.connect("baseball.db")
cursor = conn.cursor()

# Get all teams and batters
cursor.execute("SELECT DISTINCT team FROM bronze_adv_batting ORDER BY team")
teams = [row[0] for row in cursor.fetchall()]

batters = {}
for team in teams:
    cursor.execute("SELECT DISTINCT name FROM bronze_adv_batting WHERE team = ? ORDER BY name", (team,))
    batters[team] = [row[0] for row in cursor.fetchall()]

with open("static/batters.json", "w") as f:
    json.dump(batters, f, indent=2)

conn.close()
print("batters.json updated")
```

**`static/pitchers.json`** - Similar script for pitchers:
```python
# Replace 'bronze_adv_batting' with 'bronze_adv_pitching'
# Save to 'static/pitchers.json'
```

**Other JSON files** - Verify content is current:
- `batting_adv_metrics.json`
- `batting_std_metrics.json`
- `pitching_adv_metrics.json`
- `pitching_std_metrics.json`
- `batting_metrics_map.json`
- `pitching_metrics_map.json`

## Running the Application

### Start Streamlit Server

```bash
streamlit run app.py
```

**Expected Output**:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

### Access Application

1. Open browser to `http://localhost:8501`
2. Application should load automatically
3. If browser doesn't open, copy URL from terminal

### Verify Functionality

1. **Home Page**: Should load with project information
2. **Individual Batting**: 
   - Select a team (e.g., "CLEM")
   - Select a player
   - Toggle "Advanced Stats"
   - Click "Show" → Chart should appear
3. **Team Lineup**: 
   - Select a team
   - Select a stat (e.g., "AVG")
   - Set minimum PA
   - Click "Show" → Team comparison chart should appear
4. **Repeat for Pitching pages**

## Troubleshooting

### Common Issues

#### Issue: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: `sqlite3.OperationalError: no such table: bronze_adv_batting`

**Solution**: Database tables not created
```bash
python bronze/tables/create_bronze_tables.py
python silver/tables/create_silver_tables.py
```

#### Issue: `FileNotFoundError: [Errno 2] No such file or directory: 'baseball.db'`

**Solution**: Database doesn't exist
```bash
# Create tables and load data (see Initial Data Setup)
```

#### Issue: `pandas.errors.EmptyDataError: No columns to parse from file`

**Solution**: CSV files are empty or corrupted
- Re-download CSV files from Fangraphs
- Verify files are not empty: `head bronze/data/adv_batting.csv`

#### Issue: Streamlit shows blank page

**Solution**: Check browser console for errors
- Open browser Developer Tools (F12)
- Check Console tab for JavaScript errors
- Try different browser (Chrome, Firefox, Safari)

#### Issue: Port 8501 already in use

**Solution**: Kill existing Streamlit process or use different port
```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

### Performance Issues

#### Application is slow to load

**Possible Causes**:
- Large database file
- Network latency (if hosted remotely)
- Insufficient RAM

**Solutions**:
- Add database indexes (see [04-bronze-layer.md](04-bronze-layer.md))
- Implement caching (see [07-helper-functions.md](07-helper-functions.md))
- Increase system RAM

#### Charts take long to render

**Solutions**:
- Reduce data volume with stricter filters
- Use static plots (already implemented)
- Cache query results

### Data Issues

#### Players missing from dropdown

**Solution**: Regenerate `batters.json` or `pitchers.json`
```bash
# Run script from Step 5 of Initial Data Setup
```

#### Percentiles seem incorrect

**Solution**: Recalculate silver layer
```bash
python silver/process/process_adv_batting.py
python silver/process/process_std_batting.py
python silver/process/process_adv_pitching.py
python silver/process/process_std_pitching.py
```

#### Charts show no data

**Possible Causes**:
- Database not populated
- Player name mismatch
- SQL query syntax error

**Debug Steps**:
```python
import sqlite3
conn = sqlite3.connect("baseball.db")

# Check if data exists
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM bronze_adv_batting")
print(f"Total records: {cursor.fetchone()[0]}")

# Check specific player
cursor.execute("SELECT * FROM bronze_adv_batting WHERE name = 'John Smith'")
print(cursor.fetchone())

conn.close()
```

## Development Setup

### Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Testing Setup (Optional)

```bash
# Install pytest
pip install pytest

# Run tests
pytest
```

### VS Code Setup (Optional)

**Recommended Extensions**:
- Python
- Pylance
- SQLite Viewer
- Jupyter (for notebooks)

**Settings** (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

## Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Configure: `app.py` as entry point
5. Deploy

**Note**: Upload `baseball.db` separately or use external database.

### Docker

**Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run**:
```bash
docker build -t college-baseball .
docker run -p 8501:8501 college-baseball
```

### Cloud Platforms

**AWS Elastic Beanstalk**:
```bash
eb init -p python-3.9 college-baseball
eb create college-baseball-env
eb deploy
```

**Google Cloud Run**:
```bash
gcloud run deploy college-baseball \
  --source . \
  --platform managed \
  --region us-central1
```

**Azure App Service**:
```bash
az webapp up --name college-baseball \
  --resource-group baseball-rg \
  --runtime "PYTHON:3.9"
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove database (optional)
rm baseball.db

# Remove entire project directory (optional)
cd ..
rm -rf college-baseball
```
