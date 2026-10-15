from fastapi import FastAPI
from pydantic import BaseModel
from ai_analyzer import analyze_with_ai
from rag_bridge import run_rag
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import verify_password, create_access_token, decode_access_token

load_dotenv()

def get_db_connection():
    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )

    return connection

class StatusUpdate(BaseModel):
    status: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ProductionReport(BaseModel):
    problem_type: str
    problem_description: str
    downtime: int
    temperature: float
    pressure: float
    cycle_time: float
    comment: str
    ui_language: str = "en"


app = FastAPI()
security = HTTPBearer()
def require_engineer(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if payload.get("role") != "engineer":
        raise HTTPException(
            status_code=403,
            detail="Engineer access required"
        )

    return payload
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://aiproductionuiamin.z36.web.core.windows.net",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/login")
def login(login_data: LoginRequest):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, email, password_hash, role
        FROM users
        WHERE email = %s
        """,
        (login_data.email,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    user_id, email, stored_password_hash, role = user

    if not verify_password(login_data.password, stored_password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        user_id=user_id,
        email=email,
        role=role
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role
    }

@app.post("/analyze")
def analyze(report: ProductionReport):
    report_context = f"""
    Problem Type: {report.problem_type}
    Problem Description: {report.problem_description}
    Downtime: {report.downtime}
    Temperature: {report.temperature}
    Pressure: {report.pressure}
    Cycle Time: {report.cycle_time}
    Operator Comment: {report.comment}
    """

    try:
        rag_result = run_rag(report_context)

        print("\nRAG Analysis:")
        print(rag_result)

        print("\nRAG Sources:")
        print(rag_result["sources"])

    except Exception as error:
        print("\nRAG Error:")
        print(error)

        rag_result= None



    # 1. AI analysis
    result = analyze_with_ai(
        problem_type=report.problem_type,
        problem_description=report.problem_description,
        downtime=report.downtime,
        temperature=report.temperature,
        pressure=report.pressure,
        cycle_time=report.cycle_time,
        comment=report.comment,
        ui_language=report.ui_language
    )
    if rag_result is not None:
        result["severity"] = rag_result.get("severity")
        result["possible_cause"] = rag_result.get("possible_cause")
        result["recommended_action"] = rag_result.get("recommended_action")

        result["severity_reference"] = rag_result.get(
            "severity_reference"
        )

        result["possible_cause_reference"] = rag_result.get(
            "possible_cause_reference"
        )

        result["recommended_action_reference"] = rag_result.get(
            "recommended_action_reference"
        )

        result["sources"] = rag_result.get(
            "sources"
        )

        result["display_possible_cause"] = rag_result.get(
            "possible_cause"
        )

        result["display_recommended_action"] = rag_result.get(
            "recommended_action"
        )
    # 2. Connect to database
    connection = get_db_connection()
    print("DB connected")

    cursor = connection.cursor()

    # 3. Find the latest report ID
    cursor.execute(
        """
        SELECT report_id
        FROM production_reports
        WHERE report_id ~ '^RPT-[0-9]{4}$'
        ORDER BY report_id DESC
        LIMIT 1
        """
    )

    last_report = cursor.fetchone()

    # 4. Create a new report ID
    if last_report:
        last_number = int(last_report[0].split("-")[1])
        new_report_id = f"RPT-{last_number + 1:04d}"
    else:
        new_report_id = "RPT-0001"

    # 5. Create timestamp
    timestamp = datetime.now().isoformat(timespec="seconds")

    # 6. Insert new report
    cursor.execute(
        """
        INSERT INTO production_reports (
            report_id,
            timestamp,
            problem_type,
            problem_description,
            downtime_minutes,
            temperature_c,
            injection_pressure_bar,
            cycle_time_seconds,
            operator_comment,
            ai_category,
            ai_severity,
            ai_possible_cause,
            recommended_action,
            confidence,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            new_report_id,
            timestamp,
            report.problem_type,
            report.problem_description,
            report.downtime,
            report.temperature,
            report.pressure,
            report.cycle_time,
            report.comment,
            result["category"],
            result["severity"],
            result["possible_cause"],
            result["recommended_action"],
            result["confidence"],
            "OPEN"
        )
    )

    connection.commit()

    print("Data committed")
    print("Report ID:", new_report_id)

    cursor.execute("SELECT COUNT(*) FROM production_reports")
    print("Total rows in database:", cursor.fetchone()[0])

    connection.close()

    # 7. Return AI result + report metadata
    return {
        "report_id": new_report_id,
        "timestamp": timestamp,
        **result
    }


@app.get("/")
def home():
    return {
        "message": "AI Production Issue System API is running"
    }


@app.get("/reports")
def get_reports(
    severity: str | None = None,
    current_user: dict = Depends(require_engineer)
):

    connection = get_db_connection()
    cursor = connection.cursor()

    if severity:
        cursor.execute(
            """
            SELECT
                report_id,
                timestamp,
                problem_type,
                ai_severity,
                ai_category,
                confidence
            FROM production_reports
            WHERE ai_severity = %s
            ORDER BY timestamp DESC
            LIMIT 10
            """,
            (severity,)
        )

    else:
        cursor.execute(
            """
            SELECT
                report_id,
                timestamp,
                problem_type,
                ai_severity,
                ai_category,
                confidence
            FROM production_reports
            WHERE report_id IS NOT NULL
            ORDER BY timestamp DESC
            LIMIT 10
            """
        )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    reports = []

    for row in rows:
        reports.append(
            {
                "report_id": row[0],
                "timestamp": row[1],
                "problem_type": row[2],
                "severity": row[3],
                "category": row[4],
                "confidence": row[5]
            }
        )

    return reports

@app.get("/reports/{report_id}")
def get_report(
    report_id: str,
    current_user: dict = Depends(require_engineer)
):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            report_id,
            timestamp,
            problem_type,
            problem_description,
            downtime_minutes,
            temperature_c,
            injection_pressure_bar,
            cycle_time_seconds,
            operator_comment,
            ai_category,
            ai_severity,
            ai_possible_cause,
            recommended_action,
            confidence,
            status
        FROM production_reports
        WHERE report_id = %s
        """,
        (report_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return {
        "report_id": row[0],
        "timestamp": row[1],
        "problem_type": row[2],
        "problem_description": row[3],
        "downtime": row[4],
        "temperature": row[5],
        "pressure": row[6],
        "cycle_time": row[7],
        "comment": row[8],
        "category": row[9],
        "severity": row[10],
        "possible_cause": row[11],
        "recommended_action": row[12],
        "confidence": row[13],
        "status": row[14]
    }

@app.patch("/reports/{report_id}/status")
def update_report_status(
    report_id: str,
    status_update: StatusUpdate,
    current_user: dict = Depends(require_engineer)
):

    allowed_statuses = ["OPEN", "UNDER_REVIEW", "RESOLVED"]

    if status_update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE production_reports
        SET status = %s
        WHERE report_id = %s
        """,
        (status_update.status, report_id)
    )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "report_id": report_id,
        "status": status_update.status
    }