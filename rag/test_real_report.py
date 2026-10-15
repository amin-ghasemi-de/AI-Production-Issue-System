import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Resolve the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )


def get_latest_report():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT *
            FROM public.production_reports
            ORDER BY id DESC
            LIMIT 1
        """)

        report = cur.fetchone()

        if report is None:
            print("No production reports found.")
            return

        column_names = [
            description.name
            for description in cur.description
        ]

        report_data = dict(zip(column_names, report))

        print("\nLatest Production Report:")

        for key, value in report_data.items():
            print(f"{key}: {value}")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    get_latest_report()