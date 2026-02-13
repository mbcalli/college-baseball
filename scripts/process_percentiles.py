#!/usr/bin/env python3
"""Process bronze data and calculate percentiles for silver layer."""

from college_baseball.database import get_db_context
from college_baseball.processors import SilverProcessor

def main() -> None:
    """Main function."""
    print("Processing bronze data...")
    
    with get_db_context() as db:
        processor = SilverProcessor(db)
        results = processor.process_all()
    
    print("\nResults:")
    for name, count in results.items():
        print(f"  {name}: {count} records")
    
    print("\n✓ Data processed successfully")


if __name__ == "__main__":
    main()
