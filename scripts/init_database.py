#!/usr/bin/env python3
"""Initialize the database with all tables."""

from college_baseball.database import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("✓ Database initialized successfully")
