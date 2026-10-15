import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

report = """
Problem Type: Quality
Problem Description: The molded part has a short shot and is not completely filled.
Downtime: 10
Temperature: 220
Pressure: 120
Cycle Time: 42
Operator Comment: The cavity is not filling completely.
"""

severity_context = """
RULE S-06 — Confirmed production defect without documented safety hazard is MEDIUM under this project policy.

If a report clearly describes a repeatable production-quality defect such as short shots,
flash, burn marks, voids, sink marks, warpage, splay, off-color parts,
dimensional out-of-specification parts, or repeated sticking/ejection problems,
and no safety-critical condition is documented, classify severity as MEDIUM.
"""

cause_context = """
CAUSE C-01 — Short shot or incomplete fill.

Supported possible causes include insufficient shot size,
blocked or insufficient venting,
insufficient injection pressure,
injection speed that is too low,
melt temperature that is too low for the material/process window,
high material viscosity,
or flow restrictions involving the gate or runner.

CAUSE C-14 — Low injection pressure as a reported condition.

Insufficient injection pressure can contribute to short shots or incomplete fill.
Do not label pressure as low from the numeric value alone.
"""

action_context = """
ACTION A-05 — Short shot or incomplete fill: insufficient injection pressure.

Condition:
Short shot/incomplete fill is present and insufficient injection pressure is supported as the cause.

Recommended action:
Increase injection pressure within the machine, mold,
and material supplier's approved process window.

ACTION A-08 — Short shot or incomplete fill: melt too cold or injection too slow.

Condition:
The documented process window confirms melt temperature is too low,
or troubleshooting evidence indicates injection speed is too low.

Recommended action:
Adjust melt temperature or injection speed toward the approved material/process window.
"""

prompt = f"""
You are analyzing an injection molding production report.

Use ONLY the documentation provided below.

Rules:
- Do not use outside knowledge.
- Do not invent causes, limits, thresholds, or actions.
- Severity must be supported by the severity documentation.
- Possible cause must be supported by the cause documentation.
- Recommended action must be supported by the action documentation.
- A possible cause is not automatically confirmed.
- If the report does not contain enough evidence to select a specific cause, describe the documented possibilities without claiming certainty.
- If a field is not supported by the documentation, return null.
- Do not treat raw numeric values as high or low unless the documentation provides the applicable limit.
- Return valid JSON only.

Production report:
{report}

Severity documentation:
{severity_context}

Cause documentation:
{cause_context}

Action documentation:
{action_context}

Return exactly this structure:

{{
    "severity": null,
    "possible_cause": null,
    "recommended_action": null
}}
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

raw_output = response.choices[0].message.content.strip()

print("\nRAW OUTPUT")
print("=" * 60)
print(raw_output)

try:
    parsed_output = json.loads(raw_output)

    print("\nPARSED OUTPUT")
    print("=" * 60)
    print(json.dumps(parsed_output, indent=2))

except json.JSONDecodeError:
    print("\nThe model did not return valid JSON.")