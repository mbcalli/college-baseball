#!/usr/bin/env python3
"""Verify silver layer data_dates."""

from sqlalchemy import select, func
from college_baseball.database import get_db_context
from college_baseball.models import SilverAdvBatting, SilverStdBatting, SilverAdvPitching, SilverStdPitching


def main() -> None:
    """Check unique data_dates in each silver table."""
    print("=" * 70)
    print("SILVER LAYER DATA_DATE VERIFICATION")
    print("=" * 70)
    
    tables = [
        ("Silver Advanced Batting", SilverAdvBatting),
        ("Silver Standard Batting", SilverStdBatting),
        ("Silver Advanced Pitching", SilverAdvPitching),
        ("Silver Standard Pitching", SilverStdPitching),
    ]
    
    with get_db_context() as db:
        for table_name, model in tables:
            # Get unique data_dates and their counts
            result = db.execute(
                select(
                    model.data_date,
                    func.count(model.id).label('count')
                )
                .group_by(model.data_date)
                .order_by(model.data_date)
            ).all()
            
            print(f"\n{table_name}:")
            if not result:
                print("  No records found")
            else:
                total = 0
                for data_date, count in result:
                    print(f"  {data_date.strftime('%Y-%m-%d')}: {count} records")
                    total += count
                print(f"  TOTAL: {total} records")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
