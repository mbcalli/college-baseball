# Data Update Guide

## Overview

This guide walks through the complete process of updating the application with new season data. Follow these steps when:

- Starting a new season (e.g., 2026 season)
- Updating mid-season statistics
- Adding new players or teams
- Correcting data issues

## Update Schedule

### Recommended Frequency

**During Season**:
- Weekly updates for current statistics
- Daily updates during playoffs
- Real-time updates for critical games (manual)

**Off-Season**:
- Pre-season update before first game
- Post-season final update
- Roster changes as they occur

### Time Requirements

- **Full Update**: ~15 minutes (including data download)
- **Database Refresh**: ~2 minutes
- **Verification**: ~5 minutes

## Step-by-Step Update Process

### Step 1: Backup Current Data

**Why**: Preserve existing data in case something goes wrong

```bash
# Create backup directory
mkdir -p backups/$(date +%Y%m%d)

# Backup database
cp baseball.db backups/$(date +%Y%m%d)/baseball.db

# Backup CSV files
cp -r bronze/data backups/$(date +%Y%m%d)/

# Backup static files
cp -r static backups/$(date +%Y%m%d)/

echo "Backup created in backups/$(date +%Y%m%d)/"
```

**Verify Backup**:
```bash
ls -lh backups/$(date +%Y%m%d)/
```

### Step 2: Download New Data from Fangraphs

#### Access Fangraphs

1. Navigate to [Fangraphs College Leaderboard](https://www.fangraphs.com/leaders/college)
2. Log in (requires membership)

#### Download Advanced Batting

1. Select **"Advanced"** tab
2. Select **Season**: 2026 (or current season)
3. Select **Stats**: Advanced
4. Select **Qualified**: All players
5. Click **"Export Data"**
6. Save as `adv_batting.csv`
7. Move to `bronze/data/adv_batting.csv`

#### Download Standard Batting

1. Select **"Standard"** tab
2. Select **Season**: 2026
3. Select **Stats**: Standard
4. Click **"Export Data"**
5. Save as `std_batting.csv`
6. Move to `bronze/data/std_batting.csv`

#### Download Advanced Pitching

1. Select **"Pitching"** view
2. Select **"Advanced"** tab
3. Select **Season**: 2026
4. Click **"Export Data"**
5. Save as `adv_pitching.csv`
6. Move to `bronze/data/adv_pitching.csv`

#### Download Standard Pitching

1. Select **"Pitching"** view
2. Select **"Standard"** tab
3. Select **Season**: 2026
4. Click **"Export Data"**
5. Save as `std_pitching.csv`
6. Move to `bronze/data/std_pitching.csv`

#### Verify Downloads

```bash
# Check all files exist
ls -lh bronze/data/

# Check file sizes (should be >100KB each)
du -h bronze/data/*

# Preview first few lines
head -n 5 bronze/data/adv_batting.csv
```

### Step 3: Validate CSV Files

```python
# validate_csvs.py
import pandas as pd

files = {
    "Advanced Batting": "bronze/data/adv_batting.csv",
    "Standard Batting": "bronze/data/std_batting.csv",
    "Advanced Pitching": "bronze/data/adv_pitching.csv",
    "Standard Pitching": "bronze/data/std_pitching.csv"
}

for name, path in files.items():
    try:
        df = pd.read_csv(path)
        print(f"\n{name}:")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"  Sample columns: {df.columns[:5].tolist()}")
        
        # Check for expected columns
        if "Name" not in df.columns:
            print(f"  ⚠️  WARNING: 'Name' column missing!")
        if "Team" not in df.columns:
            print(f"  ⚠️  WARNING: 'Team' column missing!")
            
    except Exception as e:
        print(f"\n{name}: ❌ ERROR - {e}")

print("\n✅ Validation complete")
```

Run validation:
```bash
python validate_csvs.py
```

### Step 4: Update Bronze Layer

```bash
# Load all bronze tables
python bronze/load/load_adv_batting.py
python bronze/load/load_std_batting.py
python bronze/load/load_adv_pitching.py
python bronze/load/load_std_pitching.py
```

**Expected Output** (for each):
```
Table 'bronze_adv_batting' replaced with new data. 1247 records added.
```

**Verify Bronze Data**:
```bash
sqlite3 baseball.db << EOF
SELECT COUNT(*) as adv_batting_count FROM bronze_adv_batting;
SELECT COUNT(*) as std_batting_count FROM bronze_std_batting;
SELECT COUNT(*) as adv_pitching_count FROM bronze_adv_pitching;
SELECT COUNT(*) as std_pitching_count FROM bronze_std_pitching;
EOF
```

### Step 5: Update Silver Layer

```bash
# Process all silver tables
python silver/process/process_adv_batting.py
python silver/process/process_std_batting.py
python silver/process/process_adv_pitching.py
python silver/process/process_std_pitching.py
```

**Expected Output** (for each):
```
Table 'silver_adv_batting' replaced with new data. 1247 records added.
```

**Verify Silver Data**:
```bash
sqlite3 baseball.db << EOF
SELECT COUNT(*) as adv_batting_percentiles FROM silver_adv_batting;
SELECT COUNT(*) as std_batting_percentiles FROM silver_std_batting;
SELECT COUNT(*) as adv_pitching_percentiles FROM silver_adv_pitching;
SELECT COUNT(*) as std_pitching_percentiles FROM silver_std_pitching;
EOF
```

### Step 6: Update Static JSON Files

#### Update Team Rosters

```python
# update_rosters.py
import sqlite3
import json

conn = sqlite3.connect("baseball.db")
cursor = conn.cursor()

# Update batters.json
cursor.execute("SELECT DISTINCT team FROM bronze_adv_batting ORDER BY team")
teams = [row[0] for row in cursor.fetchall()]

batters = {}
for team in teams:
    cursor.execute("""
        SELECT DISTINCT name 
        FROM bronze_adv_batting 
        WHERE team = ? 
        ORDER BY name
    """, (team,))
    batters[team] = [row[0] for row in cursor.fetchall()]

with open("static/batters.json", "w") as f:
    json.dump(batters, f, indent=2)
print(f"✅ batters.json updated - {len(teams)} teams, {sum(len(v) for v in batters.values())} players")

# Update pitchers.json
cursor.execute("SELECT DISTINCT team FROM bronze_adv_pitching ORDER BY team")
teams = [row[0] for row in cursor.fetchall()]

pitchers = {}
for team in teams:
    cursor.execute("""
        SELECT DISTINCT name 
        FROM bronze_adv_pitching 
        WHERE team = ? 
        ORDER BY name
    """, (team,))
    pitchers[team] = [row[0] for row in cursor.fetchall()]

with open("static/pitchers.json", "w") as f:
    json.dump(pitchers, f, indent=2)
print(f"✅ pitchers.json updated - {len(teams)} teams, {sum(len(v) for v in pitchers.values())} players")

conn.close()
```

Run update:
```bash
python update_rosters.py
```

#### Verify Metric Definitions

Check that metric descriptions are still accurate:

```bash
# Review metric definitions
cat static/batting_adv_metrics.json
cat static/batting_std_metrics.json
cat static/pitching_adv_metrics.json
cat static/pitching_std_metrics.json
```

Update if Fangraphs changed any definitions.

### Step 7: Test Application

```bash
# Start application
streamlit run app.py
```

**Manual Testing Checklist**:

- [ ] Home page loads correctly
- [ ] Individual Batting:
  - [ ] Team dropdown populated
  - [ ] Player dropdown populated for selected team
  - [ ] Advanced stats chart displays correctly
  - [ ] Standard stats chart displays correctly
  - [ ] Percentile values make sense (0-100)
  - [ ] Raw values displayed correctly
- [ ] Team Lineup:
  - [ ] Team dropdown populated
  - [ ] Stat dropdown populated
  - [ ] Minimum PA filter works
  - [ ] Chart shows all qualified players
- [ ] Individual Pitching:
  - [ ] Same checks as batting
- [ ] Team Bullpen:
  - [ ] Same checks as team lineup

### Step 8: Verify Data Quality

```python
# verify_data.py
import sqlite3
import pandas as pd

conn = sqlite3.connect("baseball.db")

print("=" * 60)
print("DATA QUALITY CHECKS")
print("=" * 60)

# Check 1: Record counts match
bronze_adv_bat = pd.read_sql("SELECT COUNT(*) as count FROM bronze_adv_batting", conn).iloc[0]['count']
silver_adv_bat = pd.read_sql("SELECT COUNT(*) as count FROM silver_adv_batting", conn).iloc[0]['count']

print(f"\n1. Record Count Match:")
print(f"   Bronze adv_batting: {bronze_adv_bat}")
print(f"   Silver adv_batting: {silver_adv_bat}")
print(f"   ✅ Match" if bronze_adv_bat == silver_adv_bat else "   ❌ Mismatch")

# Check 2: Percentile distribution
percentiles = pd.read_sql("SELECT avg_percentile FROM silver_adv_batting", conn)
print(f"\n2. Percentile Distribution (should be roughly even):")
print(pd.cut(percentiles['avg_percentile'], bins=[0, 25, 50, 75, 100]).value_counts(normalize=True).sort_index())

# Check 3: Inverted metrics
data = pd.read_sql("""
    SELECT b.name, b.k_rate, s.k_rate_percentile
    FROM bronze_adv_batting b
    JOIN silver_adv_batting s ON b.id = s.id
    ORDER BY b.k_rate DESC
    LIMIT 10
""", conn)
print(f"\n3. Inverted Metric Check (K% - high K% should have LOW percentile):")
print(data)
if data['k_rate'].corr(data['k_rate_percentile']) < 0:
    print("   ✅ Correctly inverted")
else:
    print("   ❌ NOT inverted properly")

# Check 4: Outliers
outliers = pd.read_sql("""
    SELECT name, team, avg_percentile, wrc_plus_percentile
    FROM silver_adv_batting
    WHERE avg_percentile > 99 OR avg_percentile < 1
""", conn)
print(f"\n4. Outliers (>99th or <1st percentile):")
print(f"   Found {len(outliers)} outliers")
if len(outliers) > 0:
    print(outliers.head())

# Check 5: Missing values
missing = pd.read_sql("""
    SELECT 
        SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) as null_names,
        SUM(CASE WHEN team IS NULL THEN 1 ELSE 0 END) as null_teams,
        SUM(CASE WHEN avg_percentile IS NULL THEN 1 ELSE 0 END) as null_avg
    FROM silver_adv_batting
""", conn)
print(f"\n5. Missing Values:")
print(missing)
if missing.sum().sum() == 0:
    print("   ✅ No missing values")
else:
    print("   ⚠️  Missing values detected")

conn.close()
print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
```

Run verification:
```bash
python verify_data.py
```

### Step 9: Update Documentation

Update relevant documentation files:

#### `README.md`
```markdown
# college-baseball

Last updated: March 15, 2026
Current season: 2026
Data source: Fangraphs (as of March 15, 2026)
```

#### `pages/home.py`
```python
st.title("2026 College Baseball Statistics")  # Update year
```

#### `docs/README.md`
```markdown
Last updated: March 15, 2026
Current season: 2026 data
```

### Step 10: Commit Changes

```bash
# Add all changes
git add bronze/data/*.csv
git add baseball.db
git add static/*.json
git add README.md
git add pages/home.py

# Commit with descriptive message
git commit -m "Update to 2026 season data (as of March 15, 2026)"

# Push to remote
git push origin main
```

## Troubleshooting

### Issue: CSV columns don't match expected format

**Cause**: Fangraphs changed their export format

**Solution**:
1. Open CSV in Excel/LibreOffice to inspect columns
2. Update column mappings in `bronze/load/load_*.py` scripts
3. Update SQL schemas in `bronze/tables/*.sql` if needed
4. Re-run load scripts

### Issue: Percentiles all showing 50

**Cause**: All values are identical (unlikely but possible)

**Solution**:
1. Check bronze data for variation: `SELECT DISTINCT avg FROM bronze_adv_batting`
2. If no variation, check CSV import
3. Verify percentile calculation logic in `silver/process/process_*.py`

### Issue: New teams/players not appearing

**Cause**: Static JSON files not updated

**Solution**:
1. Run `update_rosters.py` script from Step 6
2. Restart Streamlit application
3. Clear browser cache if needed

### Issue: Old data still showing

**Cause**: Database not updated or cache issues

**Solution**:
```bash
# Verify database was updated
sqlite3 baseball.db "SELECT MAX(pa) FROM bronze_adv_batting;"

# If old data showing, reload
python bronze/load/load_adv_batting.py

# Restart Streamlit
pkill -f streamlit
streamlit run app.py
```

## Rollback Procedure

If update causes issues:

```bash
# Stop application
pkill -f streamlit

# Restore from backup
BACKUP_DATE=20260315  # Replace with your backup date
cp backups/$BACKUP_DATE/baseball.db ./baseball.db
cp -r backups/$BACKUP_DATE/data/* bronze/data/
cp -r backups/$BACKUP_DATE/static/* static/

# Restart application
streamlit run app.py

# Verify restoration
sqlite3 baseball.db "SELECT COUNT(*) FROM bronze_adv_batting;"
```

## Automation

### Create Update Script

```bash
#!/bin/bash
# update_data.sh - Automated data update script

set -e  # Exit on error

echo "Starting data update..."

# 1. Backup
echo "Creating backup..."
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR
cp baseball.db $BACKUP_DIR/
cp -r bronze/data $BACKUP_DIR/
cp -r static $BACKUP_DIR/
echo "✅ Backup created: $BACKUP_DIR"

# 2. Load bronze
echo "Loading bronze layer..."
python bronze/load/load_adv_batting.py
python bronze/load/load_std_batting.py
python bronze/load/load_adv_pitching.py
python bronze/load/load_std_pitching.py
echo "✅ Bronze layer loaded"

# 3. Process silver
echo "Processing silver layer..."
python silver/process/process_adv_batting.py
python silver/process/process_std_batting.py
python silver/process/process_adv_pitching.py
python silver/process/process_std_pitching.py
echo "✅ Silver layer processed"

# 4. Update rosters
echo "Updating rosters..."
python update_rosters.py
echo "✅ Rosters updated"

# 5. Verify
echo "Verifying data..."
python verify_data.py

echo "✅ Update complete!"
echo "Run 'streamlit run app.py' to start the application"
```

Make executable:
```bash
chmod +x update_data.sh
```

Run update:
```bash
# After placing new CSVs in bronze/data/
./update_data.sh
```

## Best Practices

1. **Always backup before updating**
2. **Verify CSV files before loading**
3. **Check data quality after processing**
4. **Test application before committing**
5. **Document update date in commit message**
6. **Keep backups for at least 30 days**
7. **Update documentation with new season year**
8. **Notify users of update completion**
