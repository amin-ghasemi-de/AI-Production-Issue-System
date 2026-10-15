import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY was not found.")

groq_client = Groq(api_key=GROQ_API_KEY)

def analyze_with_ai(
        problem_type,
        problem_description,
        downtime,
        temperature,
        pressure,
        cycle_time,
        comment,
        ui_language="en"
):
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
You are an industrial maintenance assistant specialized
in injection molding machines.

Validated process window for this evaluation:

- Temperature: 215–225 °C
- Injection Pressure: 75–85 bar
- Cycle Time: 38–44 seconds

Analyze the complete production issue using all available information,
including process data, problem description, downtime, and operator comment.

Do not determine severity from a single process parameter alone.

GROUND TRUTH RUBRIC v1.0

Evaluate severity using these four factors:

1. Safety / Equipment Risk — Weight ×4
0 = No safety or equipment concern
1 = Minor abnormal condition with no meaningful risk
2 = Real but non-immediate risk; maintenance/control action required
3 = Immediate/critical risk; continued operation could cause injury,
    fire, or serious equipment damage

2. Operational Impact — Weight ×3
0 = Capacity reduction <5% and no meaningful interruption
1 = Capacity reduction 5–15% or very short interruption
2 = Capacity reduction 15–30% or noticeable temporary interruption
3 = Capacity reduction >30%, full production stop, or prolonged interruption

3. Quality Impact — Weight ×3
0 = Less than 2% of parts affected
1 = 2–10% affected; minor defects
2 = 10–30% require rework or scrap
3 = More than 30% unacceptable, or severe functional/dimensional defects

4. Process Deviation — Weight ×2
0 = Critical parameters are within the validated process window and stable
1 = Near a process-window boundary or minor variation with no measurable impact
2 = Outside the validated process window with measurable production or quality impact
3 = Substantially outside the validated process window or strongly unstable,
    causing severe process or quality disruption

Calculate severity using:

weighted_score =
(Safety × 4)
+ (Operational Impact × 3)
+ (Quality Impact × 3)
+ (Process Deviation × 2)

Severity thresholds:

0–7 = LOW
8–17 = MEDIUM
18–36 = HIGH

CRITICAL OVERRIDES

Classify the issue as HIGH regardless of weighted score when a critical
override condition exists.

Safety / Equipment Override:
- Immediate safety hazard
- Fire, serious smoke, or hazardous leakage
- Immediate risk of major equipment damage
- Emergency shutdown required

Quality Override:
- Critical functional or dimensional defect that makes the product
  unsafe or unusable
- Catastrophic reject/scrap condition

Operational Override:
- Prolonged full production shutdown
- Critically collapsed production capacity

A factor score of 3 alone does NOT automatically activate an override.

Use one category:
Mechanical
Electrical
Process
Quality
Tooling
Unknown

Use one severity:
LOW
MEDIUM
HIGH

recommended_action must be a short practical next step for the
operator or maintenance technician.

confidence must be an integer from 0 to 100 representing the model's confidence percentage.
Example: 85 means 85% confidence.

Return ONLY valid JSON with:

category
severity
possible_cause
recommended_action
confidence
"""
            },
            {
                "role": "user",
                "content": f"""
Problem Type: {problem_type}
Problem Description: {problem_description}
Downtime: {downtime} minutes
Temperature: {temperature} °C
Injection Pressure: {pressure} bar
Cycle Time: {cycle_time} seconds
Operator Comment: {comment}
UI Language: {ui_language}

Analyze all information together.
LANGUAGE RULES:

All canonical analysis fields must ALWAYS be written in English,
regardless of the operator's interface language.

The following fields must always remain in English:
- category
- severity
- possible_cause
- recommended_action

These canonical fields will be stored in the database.

If ui_language is "de":
- also return display_possible_cause in German
- also return display_recommended_action in German

If ui_language is "en":
- display_possible_cause must be identical to possible_cause
- display_recommended_action must be identical to recommended_action

The severity value must always remain exactly one of:
LOW, MEDIUM, HIGH

Return only valid JSON.
"""
            }
        ],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)

    confidence = result.get("confidence", 0)

    if isinstance(confidence, float) and 0 <= confidence <= 1:
        confidence = round(confidence * 100)

    elif isinstance(confidence, (int, float)) and 0 <= confidence <= 10:
        confidence = round(confidence * 10)

    elif isinstance(confidence, str) and "/10" in confidence:
        confidence = round(float(confidence.split("/")[0]) * 10)

    else:
        confidence = round(float(confidence))

    result["confidence"] = max(0, min(100, confidence))

    return result