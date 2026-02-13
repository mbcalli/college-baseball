#!/usr/bin/env python3
"""Load all CSV data into bronze layer."""

import sys
from pathlib import Path

from college_baseball.config import get_settings
from college_baseball.database import get_db_context
from college_baseball.loaders import DataLoader

def main() -> None:
    """Main function."""
    settings = get_settings()
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else settings.bronze_dir
    
    if not data_dir.exists():
        print(f"Error: Directory not found: {data_dir}")
        sys.exit(1)
    
    print(f"Loading data from {data_dir}...")
    
    with get_db_context() as db:
        loader = DataLoader(db)
        results = loader.load_all(data_dir)
    
    print("\nResults:")
    for name, count in results.items():
        print(f"  {name}: {count} records")
    
    print("\n✓ Data loaded successfully")


if __name__ == "__main__":
    main()
