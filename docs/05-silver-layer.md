# Silver Layer

## Purpose

The silver layer transforms bronze layer data into percentile-ranked metrics, making it easy to compare players across different statistics on a normalized 0-100 scale.

## Directory Structure

```
silver/
├── process/                      # Percentile calculation scripts
│   ├── process_adv_batting.py
│   ├── process_adv_pitching.py
│   ├── process_std_batting.py
│   └── process_std_pitching.py
└── tables/                       # SQL schemas
    ├── create_silver_tables.py
    ├── silver_adv_batting.sql
    ├── silver_adv_pitching.sql
    ├── silver_std_batting.sql
    └── silver_std_pitching.sql
```

## Core Concept: Percentile Ranking

### What is a Percentile?

A percentile indicates the percentage of values that fall below a given value:
- **99th percentile**: Better than 99% of players
- **75th percentile**: Better than 75% of players
- **50th percentile**: Median (average)
- **25th percentile**: Better than only 25% of players

### Why Use Percentiles?

1. **Normalization**: Different stats have different scales (AVG ~0.300, wRC+ ~100)
2. **Comparability**: Compare apples-to-apples across metrics
3. **Intuitive**: Easy to understand relative performance
4. **Consistent**: Same interpretation across all statistics

## Table Schemas

### `silver_adv_batting`

```sql
CREATE TABLE IF NOT EXISTS silver_adv_batting (
    id TEXT PRIMARY KEY,
    name TEXT,
    team TEXT,
    pa_percentile INT,
    bb_rate_percentile INT,
    k_rate_percentile INT,
    bb_per_k_percentile INT,
    avg_percentile INT,
    obp_percentile INT,
    slg_percentile INT,
    ops_percentile INT,
    iso_percentile INT,
    spd_percentile INT,
    babip_percentile INT,
    wsb_percentile INT,
    wrc_percentile INT,
    wraa_percentile INT,
    woba_percentile INT,
    wrc_plus_percentile INT
)
```

### `silver_std_batting`

```sql
CREATE TABLE IF NOT EXISTS silver_std_batting (
    id TEXT PRIMARY KEY,
    name TEXT,
    team TEXT,
    g_percentile INT,
    ab_percentile INT,
    pa_percentile INT,
    h_percentile INT,
    single_percentile INT,
    double_percentile INT,
    triple_percentile INT,
    hr_percentile INT,
    r_percentile INT,
    rbi_percentile INT,
    bb_percentile INT,
    ibb_percentile INT,
    so_percentile INT,
    hbp_percentile INT,
    sf_percentile INT,
    sh_percentile INT,
    gdp_percentile INT,
    sb_percentile INT,
    cs_percentile INT,
    avg_percentile INT
)
```

Similar schemas exist for `silver_adv_pitching` and `silver_std_pitching`.

## Processing Scripts

### Standard Processing Flow

Each processing script follows this pattern:

```python
import pandas as pd
import numpy as np
import sqlite3

# 1. Connect to database
connection = sqlite3.connect("baseball.db")

# 2. Read bronze data
data = pd.read_sql("SELECT * FROM bronze_adv_batting", connection)

# 3. Define columns to percentile-rank
columns_to_percentile = [
    "pa", "bb_rate", "k_rate", "bb_per_k", "avg", "obp", 
    "slg", "ops", "iso", "spd", "babip", "wsb", "wrc", 
    "wraa", "woba", "wrc_plus"
]

# 4. Define inverted metrics (lower is better)
lower_is_better = ["k_rate"]

# 5. Calculate percentiles
percentile_columns = [f"{col}_percentile" for col in columns_to_percentile]

for column, percentile_col in zip(columns_to_percentile, percentile_columns):
    # Invert if lower is better
    k = -1 if column in lower_is_better else 1
    
    # Calculate percentile rank (0.0 to 1.0)
    data[percentile_col] = (k * data[column]).rank(pct=True)
    
    # Convert to 0-100 scale
    data[percentile_col] = 100 * data[percentile_col]
    
    # Convert to integer
    data[percentile_col] = data[percentile_col].astype(int)

# 6. Keep only id, name, team, and percentiles
data = data[["id", "name", "team"] + percentile_columns]

# 7. Write to silver table
data.to_sql("silver_adv_batting", connection, 
            if_exists="replace", index=False)

connection.close()

print(f"Table 'silver_adv_batting' replaced with new data. {len(data)} records added.")
```

## Inverted Metrics

Some statistics are **better when lower**. The system inverts these so higher percentiles always mean better performance.

### Batting - Inverted Metrics

**Advanced Batting**:
- `k_rate`: Lower strikeout rate is better

**Standard Batting**:
- `so`: Fewer strikeouts is better
- `gdp`: Fewer double plays is better
- `cs`: Fewer caught stealing is better

### Pitching - Inverted Metrics

**Advanced Pitching**:
- `bb_per_9`: Fewer walks per 9 innings is better
- `hr_per_9`: Fewer home runs per 9 innings is better
- `babip`: Lower BABIP suggests luck (though complex interpretation)
- `hr_per_fb`: Fewer home runs per fly ball is better
- `era`: Lower ERA is better
- `fip`: Lower FIP is better
- `xfip`: Lower xFIP is better
- `siera`: Lower SIERA is better

**Standard Pitching**:
- `l`: Fewer losses is better
- `era`: Lower ERA is better
- `h`: Fewer hits allowed is better
- `r`: Fewer runs allowed is better
- `er`: Fewer earned runs allowed is better
- `hr`: Fewer home runs allowed is better
- `bb`: Fewer walks is better
- `ibb`: Fewer intentional walks is better
- `hbp`: Fewer hit batters is better
- `wp`: Fewer wild pitches is better
- `bk`: Fewer balks is better

### Implementation

```python
# Example for advanced batting
lower_is_better = ["k_rate"]

for column_to_percentile, percentile_column in zip(columns_to_percentile, percentile_columns):
    if column_to_percentile in lower_is_better:
        k = -1  # Invert the metric
    else:
        k = 1   # Standard calculation
    
    data[percentile_column] = (k * data[column_to_percentile]).rank(pct=True)
    data[percentile_column] = 100 * data[percentile_column]
    data[percentile_column] = data[percentile_column].astype(int)
```

## Percentile Calculation Details

### Pandas `.rank()` Method

```python
data['stat_percentile'] = data['stat'].rank(pct=True)
```

**Parameters**:
- `pct=True`: Returns percentile rank (0.0 to 1.0) instead of ordinal rank
- Default method: `'average'` - assigns average rank to ties

**Example**:
```
Values: [10, 20, 30, 40, 50]
Ranks:  [0.2, 0.4, 0.6, 0.8, 1.0]
Scaled: [20,  40,  60,  80,  100]
```

### Handling Ties

When multiple players have identical values, `.rank(pct=True)` assigns the average percentile:

```
Values: [10, 20, 20, 30]
Ranks:  [0.25, 0.625, 0.625, 1.0]  # 0.625 = average of 0.5 and 0.75
Scaled: [25,   62,    62,    100]
```

### Edge Cases

**All Same Value**:
```python
# If all players have same value, all get 50th percentile
data = [100, 100, 100, 100]
percentiles = [50, 50, 50, 50]
```

**Missing Values**:
```python
# NaN values are ignored in ranking
data = [10, NaN, 30, 40]
percentiles = [25, NaN, 67, 100]
```

## Data Validation

### Expected Results

After processing, verify:

```sql
-- Check percentile distribution (should be roughly uniform)
SELECT 
    CASE 
        WHEN avg_percentile BETWEEN 0 AND 25 THEN '0-25'
        WHEN avg_percentile BETWEEN 26 AND 50 THEN '26-50'
        WHEN avg_percentile BETWEEN 51 AND 75 THEN '51-75'
        ELSE '76-100'
    END as quartile,
    COUNT(*) as count
FROM silver_adv_batting
GROUP BY quartile;

-- Verify inverted metrics (high K% should have low percentile)
SELECT 
    name, 
    k_rate,
    k_rate_percentile
FROM bronze_adv_batting b
JOIN silver_adv_batting s ON b.id = s.id
ORDER BY k_rate DESC
LIMIT 10;

-- Check for outliers
SELECT name, team, avg_percentile 
FROM silver_adv_batting 
WHERE avg_percentile > 95 OR avg_percentile < 5;
```

### Validation Queries

```python
# Python validation script
import pandas as pd
import sqlite3

conn = sqlite3.connect("baseball.db")

# Load both layers
bronze = pd.read_sql("SELECT * FROM bronze_adv_batting", conn)
silver = pd.read_sql("SELECT * FROM silver_adv_batting", conn)

# Merge for comparison
merged = bronze.merge(silver, on='id', suffixes=('_bronze', '_silver'))

# Check K% inversion: high K% → low percentile
print("K% Inversion Check (should be negative correlation):")
print(merged[['k_rate', 'k_rate_percentile']].corr())

# Check AVG: high AVG → high percentile
print("\nAVG Check (should be positive correlation):")
print(merged[['avg', 'avg_percentile']].corr())

# Check percentile distribution
print("\nPercentile distribution (should be roughly 25% in each quartile):")
print(pd.cut(merged['avg_percentile'], bins=[0, 25, 50, 75, 100]).value_counts(normalize=True))

conn.close()
```

## Performance Considerations

### Current Performance

- **Dataset Size**: ~1,000-2,000 players per category
- **Processing Time**: <1 second per table
- **Memory Usage**: Minimal (entire dataset fits in RAM)

### Optimization Opportunities

If processing becomes slow:

1. **Vectorization**: Already using pandas vectorized operations
2. **Chunking**: Process in batches if dataset grows significantly
3. **Caching**: Store percentiles and only recalculate for new players
4. **Parallel Processing**: Process multiple tables simultaneously

### Scalability

The current approach scales linearly with player count:
- 1,000 players: ~0.5 seconds
- 10,000 players: ~5 seconds
- 100,000 players: ~50 seconds

No optimization needed for foreseeable future.

## Maintenance

### Adding New Metrics

To add a new metric to percentile calculation:

1. Ensure metric exists in bronze table
2. Add to `columns_to_percentile` list
3. If lower is better, add to `lower_is_better` list
4. Update silver table schema (add `{metric}_percentile INT`)
5. Run processing script

### Changing Percentile Calculation

To use different percentile method (e.g., handle ties differently):

```python
# Current method
data['stat_percentile'] = data['stat'].rank(pct=True, method='average')

# Alternative: minimum rank for ties
data['stat_percentile'] = data['stat'].rank(pct=True, method='min')

# Alternative: maximum rank for ties
data['stat_percentile'] = data['stat'].rank(pct=True, method='max')
```

### Recalculating Percentiles

To recalculate percentiles without reloading bronze data:

```bash
# Run all processing scripts
python silver/process/process_adv_batting.py
python silver/process/process_std_batting.py
python silver/process/process_adv_pitching.py
python silver/process/process_std_pitching.py
```

No need to reload CSVs or bronze tables.
