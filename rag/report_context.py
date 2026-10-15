
def build_report_context(report):
    fields = [
        ("Problem Description", report.get("problem_description")),
        ("Downtime", report.get("downtime")),
        ("Temperature", report.get("temperature")),
        ("Pressure", report.get("pressure")),
        ("Cycle Time", report.get("cycle_time")),
        ("Operator Comment", report.get("comment")),
    ]

    lines = []

    for label, value in fields:
        if value is not None and value != "":
            lines.append(f"{label}: {value}")

    return "\n".join(lines)
