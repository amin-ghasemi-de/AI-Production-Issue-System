from rag_bridge import run_rag


input_text = """
Problem Type: Quality
Problem Description: The molded part has a short shot and is not completely filled.
Downtime: 10
Temperature: 220
Pressure: 120
Cycle Time: 42
Operator Comment: Injection pressure is below the approved process window.
"""

result = run_rag(input_text)

print("\nRAG RESULT")
print("=" * 60)

print(result)