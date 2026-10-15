import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    sslmode="require"
)

print("Connected to Azure PostgreSQL! ✅")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS production_reports (
        report_id TEXT PRIMARY KEY,
        timestamp TIMESTAMP,
        machine_id TEXT,
        problem_type TEXT,
        problem_description TEXT,
        downtime_minutes INTEGER,
        temperature_c REAL,
        injection_pressure_bar REAL,
        cycle_time_seconds REAL,
        operator_comment TEXT,
        rule_based_severity TEXT,
        ai_category TEXT,
        ai_severity TEXT,
        ai_possible_cause TEXT,
        recommended_action TEXT,
        confidence INTEGER,
        final_severity TEXT,
        status TEXT
    );
""")

conn.commit()

print("production_reports table created! ✅")

cursor.close()
conn.close()