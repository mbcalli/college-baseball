# Scripts Directory

This directory contains executable Python scripts that use the `college_baseball` package.

## Available Scripts

### Database Management

- **`init_database.py`**: Initialize the database with all tables
  ```bash
  python scripts/init_database.py
  ```

### Data Loading

- **`load_data.py`**: Load CSV files into bronze layer
  ```bash
  python scripts/load_data.py [data_directory]
  ```

- **`process_percentiles.py`**: Calculate percentiles for silver layer
  ```bash
  python scripts/process_percentiles.py
  ```

- **`full_update.py`**: Complete update pipeline (init + load + process)
  ```bash
  python scripts/full_update.py [data_directory]
  ```

### API Server

- **`start_api.py`**: Start the FastAPI development server
  ```bash
  python scripts/start_api.py
  ```

## Using the CLI

Alternatively, use the CLI tool installed with the package:

```bash
# Initialize database
college-baseball init

# Load data
college-baseball load --data-dir data/bronze

# Process percentiles
college-baseball process

# Full update
college-baseball update --data-dir data/bronze

# Start API server
college-baseball serve --reload
```

## Development

All scripts import from the `college_baseball` package, so make sure the package is installed:

```bash
# Using uv
uv pip install -e .

# Or with pip
pip install -e .
```
