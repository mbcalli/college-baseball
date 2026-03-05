#!/usr/bin/env python3
"""Reset database: drop all tables, reinitialize, and reload data.

WARNING: This script will DELETE ALL DATA in the database before reloading.
Use with extreme caution in production!

Usage:
    python scripts/reset_database.py data/upload_02_16_2026
    python scripts/reset_database.py data/upload_02_13_2026 data/upload_02_16_2026
"""

import re
import sys
from datetime import datetime
from pathlib import Path

from college_baseball.config import get_settings
from college_baseball.database import drop_all_tables, get_db_context, init_db
from college_baseball.loaders import DataLoader
from college_baseball.processors import SilverProcessor


def parse_date_from_folder(folder_path: Path) -> datetime:
    """Extract date from folder name like 'upload_02_16_2026'.
    
    Falls back to current time if date cannot be parsed.
    """
    folder_name = folder_path.name
    
    # Try to match pattern: upload_MM_DD_YYYY or similar
    match = re.search(r'(\d{2})_(\d{2})_(\d{4})', folder_name)
    
    if match:
        month, day, year = match.groups()
        try:
            return datetime(int(year), int(month), int(day))
        except ValueError:
            pass
    
    # Fallback to current time
    return datetime.utcnow()


def main() -> None:
    """Main function."""
    if len(sys.argv) < 2:
        print("Error: Please provide at least one data directory")
        print("\nUsage:")
        print("  python scripts/reset_database.py data/upload_02_16_2026")
        print("  python scripts/reset_database.py data/upload_02_13_2026 data/upload_02_16_2026")
        sys.exit(1)
    
    settings = get_settings()
    data_dirs = [Path(arg) for arg in sys.argv[1:]]
    
    # Validate all directories exist
    for data_dir in data_dirs:
        if not data_dir.exists():
            print(f"Error: Directory not found: {data_dir}")
            sys.exit(1)
    
    print("=" * 70)
    print("⚠️  DATABASE RESET - WARNING ⚠️")
    print("=" * 70)
    print(f"\nDatabase: {settings.database_url}")
    print(f"\nThis will:")
    print("  1. DROP ALL TABLES (delete all existing data)")
    print("  2. Recreate tables")
    print("  3. Load data from:")
    for data_dir in data_dirs:
        print(f"     - {data_dir}")
    print("  4. Process percentiles")
    
    # Safety confirmation
    print("\n" + "=" * 70)
    response = input("Are you sure you want to proceed? Type 'YES' to continue: ")
    
    if response != "YES":
        print("\nAborted. No changes were made.")
        sys.exit(0)
    
    print("\n" + "=" * 70)
    print("PROCEEDING WITH DATABASE RESET")
    print("=" * 70)
    
    # Step 1: Drop all tables
    print("\n[1/4] Dropping all tables...")
    drop_all_tables()
    print("✓ All tables dropped")
    
    # Step 2: Recreate tables
    print("\n[2/4] Recreating tables...")
    init_db()
    print("✓ Tables recreated")
    
    # Step 3: Load data from all directories
    print(f"\n[3/4] Loading data from {len(data_dirs)} director{'y' if len(data_dirs) == 1 else 'ies'}...")
    total_records = {}
    
    for i, data_dir in enumerate(data_dirs, 1):
        data_date = parse_date_from_folder(data_dir)
        print(f"\n  Loading from {data_dir} ({i}/{len(data_dirs)})...")
        print(f"    Using data_date: {data_date.strftime('%Y-%m-%d')}")
        with get_db_context() as db:
            loader = DataLoader(db)
            load_results = loader.load_all(data_dir, data_date=data_date)
        
        for name, count in load_results.items():
            total_records[name] = total_records.get(name, 0) + count
            print(f"    ✓ {name}: {count} records")
    
    print("\n  Total records loaded:")
    for name, count in total_records.items():
        print(f"    {name}: {count} records")
    
    # Step 4: Process percentiles
    print("\n[4/4] Processing percentiles...")
    with get_db_context() as db:
        processor = SilverProcessor(db)
        process_results = processor.process_all()
    
    for name, count in process_results.items():
        print(f"  ✓ {name}: {count} records")
    
    print("\n" + "=" * 70)
    print("✓ DATABASE RESET COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()
