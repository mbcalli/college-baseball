# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Backend (Python / uv)

```bash
# Install dependencies
uv sync

# Run API locally (with reload)
uv run uvicorn college_baseball.api:app --reload
# or
uv run college-baseball serve --reload

# CLI commands
uv run college-baseball init           # Create DB tables
uv run college-baseball load           # Load all upload_MM_DD_YYYY folders in data/
uv run college-baseball process        # Calculate percentiles (latest date only)
uv run college-baseball process --all  # Calculate percentiles for all dates
uv run college-baseball load-and-process  # Full rebuild: drop tables, reload all, process all
uv run college-baseball update         # Incremental: load + process (does not drop tables)

# Scripts (alternative to CLI)
uv run python scripts/full_update.py data/upload_02_26_2026
uv run python scripts/reset_database.py data/upload_02_16_2026 data/upload_02_26_2026

# Linting / formatting
uv run ruff check src/
uv run black src/
uv run mypy src/

# Tests
uv run pytest
uv run pytest tests/test_foo.py::TestBar::test_baz  # Single test
```

### Frontend (Node / npm)

```bash
cd frontend
npm install
npm run dev      # Dev server at http://localhost:5173
npm run build    # Production build → frontend/dist/
npm run preview  # Preview production build
```

## Architecture

### Overview

A college baseball stats app (data from Fangraphs) with a **Bronze/Silver medallion data pipeline**, a FastAPI backend, and a React + TypeScript frontend. Deployed on AWS (Lambda + RDS for backend, S3 + CloudFront for frontend).

### Data Pipeline

Raw Fangraphs CSV exports are placed in date-stamped folders (`data/upload_MM_DD_YYYY/`) containing four files: `adv_batting.csv`, `std_batting.csv`, `adv_pitching.csv`, `std_pitching.csv`.

1. **Bronze layer** (`DataLoader` in `src/college_baseball/loaders.py`): CSVs are loaded into `bronze_adv_batting`, `bronze_std_batting`, `bronze_adv_pitching`, `bronze_std_pitching` tables. The folder name date becomes `data_date`, enabling multi-season storage.

2. **Silver layer** (`SilverProcessor` in `src/college_baseball/processors.py`): Reads bronze rows grouped by `data_date`, computes percentile rankings via `processing.py` (`calculate_percentiles` with `invert=True` for lower-is-better stats like ERA, K%), and writes results to `silver_*` tables. Silver tables store only `id`, `name`, `team`, `data_date`, and `*_percentile` columns.

Primary keys for all bronze/silver tables are composite: `(id, data_date)`, where `id` maps to Fangraphs `PlayerId`.

### Backend (`src/college_baseball/`)

- `config.py` — Pydantic `Settings` loaded from `.env`. Key vars: `DATABASE_URL`, `CORS_ORIGINS`.
- `database.py` — SQLAlchemy engine + `get_db()` dependency + `get_db_context()` context manager.
- `models.py` — SQLAlchemy ORM models for all 8 tables (4 bronze, 4 silver).
- `schemas.py` — Pydantic response models for the API.
- `api.py` — FastAPI app. All data queries filter to the **latest `data_date`** for a given year (or overall). Includes a Mangum `handler` for Lambda deployment.
- `cli.py` — Typer CLI wrapping the pipeline operations.

The API year-filters by finding `max(data_date)` per year from `bronze_adv_batting`, so adding a new upload folder automatically makes it the "current" snapshot for that season.

### Frontend (`frontend/src/`)

React + TypeScript + Vite. Uses React Router for navigation.

- `api.ts` — Axios client; reads `VITE_API_URL` env var (falls back to `http://localhost:8000`).
- Pages: `IndividualBatting`, `IndividualPitching`, `TeamBatting`, `TeamPitching`, `CompareBatting`, `ComparePitching`, `Home`.
- Key components: `StatBar` (Recharts horizontal bar showing percentile with blue→red color scale), `RadarChart`, `Toggle`, `DataStatusTerminal`.
- Each player/team page follows the same pattern: select year → select team → select player → fetch profile with `{statistics: [{name, value, formatted_value, percentile}]}`.

### Dual Source: `src/` vs `lambda_package/`

`lambda_package/` is a vendored copy of the Python package (plus dependencies like FastAPI, numpy, pydantic-settings, starlette) bundled for AWS Lambda. When you change backend code in `src/college_baseball/`, you must also update `lambda_package/college_baseball/` and rebuild `lambda_package.zip` via `bash scripts/deploy_lambda_pip.sh` before deploying.

### Deployment (Production)

- **Backend**: AWS Lambda (`college-baseball-api`) + API Gateway at `https://u562ohuajf.execute-api.us-east-1.amazonaws.com/default`
- **Frontend**: S3 bucket `college-baseball` behind CloudFront at `https://d5qhrmztf8nsl.cloudfront.net`
- **Database**: PostgreSQL RDS at `college-baseball-db.ct0mmoymk3ee.us-east-1.amazonaws.com:5432`, database `baseball`
- Lambda env vars: `DATABASE_URL` (PostgreSQL connection string), `CORS_ORIGINS=*`
- After frontend deploy: invalidate CloudFront cache with `aws cloudfront create-invalidation --distribution-id d5qhrmztf8nsl --paths "/*"`

### Configuration

`.env` file (not committed) controls local settings. The `Settings` class (`config.py`) uses `CORS_ORIGINS` env var which accepts `*`, a comma-separated list, or a JSON array of origins.
