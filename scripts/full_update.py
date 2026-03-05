#!/usr/bin/env python3
"""Full update: initialize database, load data, and process percentiles."""

import re
import sys
from datetime import datetime
from pathlib import Path

from college_baseball.config import get_settings
from college_baseball.database import get_db_context, init_db
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
    settings = get_settings()
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else settings.bronze_dir
    
    if not data_dir.exists():
        print(f"Error: Directory not found: {data_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print("FULL DATABASE UPDATE")
    print("=" * 60)
    
    # Step 1: Initialize database
    print("\n[1/3] Initializing database...")
    init_db()
    print("✓ Database initialized")
    
    # Step 2: Load bronze data
    data_date = parse_date_from_folder(data_dir)
    print(f"\n[2/3] Loading data from {data_dir}...")
    print(f"Using data_date: {data_date.strftime('%Y-%m-%d')}")
    with get_db_context() as db:
        loader = DataLoader(db)
        load_results = loader.load_all(data_dir, data_date=data_date)
    
    for name, count in load_results.items():
        print(f"  ✓ {name}: {count} records")
    
    # Step 3: Process silver data
    print("\n[3/3] Processing percentiles...")
    with get_db_context() as db:
        processor = SilverProcessor(db)
        process_results = processor.process_all()
    
    for name, count in process_results.items():
        print(f"  ✓ {name}: {count} records")
    
    print("\n" + "=" * 60)
    print("✓ FULL UPDATE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
