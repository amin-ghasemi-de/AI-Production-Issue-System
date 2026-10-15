import json

from ai_analyzer import analyze_with_ai


with open("evaluation_dataset.json", "r", encoding="utf-8") as file:
    dataset = json.load(file)
print("Number of test cases:", len(dataset))
results = []
correct = 0

for case in dataset:
    print(f"\nRunning case {case['id']}...")

    ai_result = analyze_with_ai(
        problem_type=case["problem_type"],
        problem_description=case["problem_description"],
        downtime=case["downtime"],
        temperature=case["temperature"],
        pressure=case["pressure"],
        cycle_time=case["cycle_time"],
        comment=case["comment"]
    )

    prediction = ai_result["severity"]
    reference = case["reference_severity"]

    is_correct = prediction == reference

    if is_correct:
        correct += 1

    results.append({
        "id": case["id"],
        "reference_severity": reference,
        "predicted_severity": prediction,
        "correct": is_correct
    })

    print("Reference Severity:", reference)
    print("AI Severity:", prediction)
    print("AI Category:", ai_result["category"])
    print("Confidence:", ai_result["confidence"])


accuracy = correct / len(dataset)

print(f"\nAccuracy: {accuracy:.2%}")
print("\nWrong predictions:")

for result in results:
    if not result["correct"]:
        print(
            f"Case {result['id']}: "
            f"Reference={result['reference_severity']} | "
            f"Predicted={result['predicted_severity']}"
        )
labels = ["LOW", "MEDIUM", "HIGH"]

confusion_matrix = {
    actual: {predicted: 0 for predicted in labels}
    for actual in labels
}

for result in results:
    actual = result["reference_severity"]
    predicted = result["predicted_severity"]

    confusion_matrix[actual][predicted] += 1
print("\nConfusion Matrix:")
print("           Predicted")
print("           LOW  MEDIUM  HIGH")

for actual in labels:
    print(
        f"{actual:<7}   "
        f"{confusion_matrix[actual]['LOW']:^5} "
        f"{confusion_matrix[actual]['MEDIUM']:^7} "
        f"{confusion_matrix[actual]['HIGH']:^5}"
    )
# ======================================
# Precision / Recall for HIGH
# ======================================

tp_high = confusion_matrix["HIGH"]["HIGH"]

fn_high = (
    confusion_matrix["HIGH"]["LOW"] +
    confusion_matrix["HIGH"]["MEDIUM"]
)

fp_high = (
    confusion_matrix["LOW"]["HIGH"] +
    confusion_matrix["MEDIUM"]["HIGH"]
)

recall_high = tp_high / (tp_high + fn_high)
precision_high = tp_high / (tp_high + fp_high)

f1_high = 2 * (precision_high * recall_high) / (precision_high + recall_high)

print("\nMetrics for HIGH severity:")
print(f"Recall (HIGH): {recall_high:.2%}")
print(f"Precision (HIGH): {precision_high:.2%}")
print(f"F1 Score (HIGH): {f1_high:.2%}")