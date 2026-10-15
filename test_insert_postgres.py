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

cursor = conn.cursor()

cursor.execute("""
    INSERT INTO production_reports (
        report_id,
        timestamp,
        machine_id,
        problem_type,
        problem_description,
        downtime_minutes,
        temperature_c,
        injection_pressure_bar,
        cycle_time_seconds,
        operator_comment,
        rule_based_severity,
        ai_category,
        ai_severity,
        ai_possible_cause,
        recommended_action,
        confidence,
        final_severity,
        status
    )
    VALUES (
        'RPT-CLOUD-TEST-001',
        CURRENT_TIMESTAMP,
        'IMM-01',
        'Pressure issue',
        'Injection pressure dropped during production',
        15,
        220,
        70,
        41,
        'Test report for Azure PostgreSQL',
        'MEDIUM',
        'Process',
        'MEDIUM',
        'Possible pressure instability',
        'Check hydraulic pressure system',
        85,
        'MEDIUM',
        'OPEN'
    )
    ON CONFLICT (report_id) DO NOTHING;
""")

conn.commit()

cursor.execute("""
    SELECT report_id, machine_id, final_severity, status
    FROM production_reports
    WHERE report_id = 'RPT-CLOUD-TEST-001';
""")

row = cursor.fetchone()

print("Saved row:", row)

cursor.close()
conn.close()