import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from groq import Groq


PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

chroma_client = chromadb.PersistentClient(
    path=str(PROJECT_ROOT / "chroma_db")
)

collection = chroma_client.get_collection(
    name="production_knowledge"
)


def semantic_retrieve(input_text, document_type, n_results=10):
    return collection.query(
        query_texts=[input_text],
        n_results=n_results,
        where={
            "document_type": document_type
        }
    )


def keyword_match(document_type, keyword):
    stored = collection.get(
        where={
            "document_type": document_type
        },
        include=[
            "documents",
            "metadatas"
        ]
    )

    matches = []

    for document, metadata in zip(
        stored["documents"],
        stored["metadatas"]
    ):
        if keyword.lower() in document.lower():
            matches.append(
                {
                    "document": document,
                    "metadata": metadata
                }
            )

    return matches


def detect_issue_keyword(text):
    issue_terms = [
        "flash",
        "short shot",
        "burn marks",
        "voids",
        "sink marks",
        "warpage",
        "splay",
        "off-color",
        "part sticking",
        "ejector-pin marks",
        "nozzle drool",
        "long cycle time",
        "cooling problem",
        "dimensional out-of-specification",
    ]

    text_lower = text.lower()

    for term in issue_terms:
        if term in text_lower:
            return term

    return None


def clean_semantic_results(documents, metadatas):
    cleaned = []

    for document, metadata in zip(
        documents,
        metadatas
    ):
        if document.startswith("SOURCE NOTE"):
            continue

        if document.startswith("DOCUMENT_TYPE"):
            continue

        cleaned.append(
            {
                "document": document,
                "metadata": metadata
            }
        )

    return cleaned


def merge_results(
    semantic_documents,
    semantic_metadatas,
    keyword_results,
    limit=3
):
    merged = []
    seen = set()

    for item in keyword_results:
        document = item["document"]

        if document not in seen:
            merged.append(item)
            seen.add(document)

    semantic_results = clean_semantic_results(
        semantic_documents,
        semantic_metadatas
    )

    for item in semantic_results:
        document = item["document"]

        if document not in seen:
            merged.append(item)
            seen.add(document)

    return merged[:limit]


def build_context(results):
    return "\n\n".join(
        item["document"]
        for item in results
    )


def get_sources(results):
    sources = []

    for item in results:
        source = item["metadata"].get("source")

        if source and source not in sources:
            sources.append(source)

    return sources


report = """
Problem Type: Quality
Problem Description: The molded part has a short shot and is not completely filled.
Downtime: 10
Temperature: 220
Pressure: 120
Cycle Time: 42
Operator Comment: Injection pressure is below the approved process window.
"""

detected_keyword = detect_issue_keyword(report)

print("\nDetected keyword:", detected_keyword)


severity_results = semantic_retrieve(
    input_text=report,
    document_type="severity",
    n_results=10
)

severity_keyword_results = []

if detected_keyword:
    severity_keyword_results = keyword_match(
        document_type="severity",
        keyword=detected_keyword
    )

severity_final = merge_results(
    severity_results["documents"][0],
    severity_results["metadatas"][0],
    severity_keyword_results,
    limit=3
)


cause_results = semantic_retrieve(
    input_text=report,
    document_type="cause",
    n_results=10
)

cause_keyword_results = []

if detected_keyword:
    cause_keyword_results = keyword_match(
        document_type="cause",
        keyword=detected_keyword
    )

cause_final = merge_results(
    cause_results["documents"][0],
    cause_results["metadatas"][0],
    cause_keyword_results,
    limit=3
)


action_results = semantic_retrieve(
    input_text=report,
    document_type="action",
    n_results=5
)

action_cleaned = clean_semantic_results(
    action_results["documents"][0],
    action_results["metadatas"][0]
)

action_final = action_cleaned[:3]


severity_context = build_context(
    severity_final
)

cause_context = build_context(
    cause_final
)

action_context = build_context(
    action_final
)


sources = {
    "severity": get_sources(
        severity_final
    ),
    "possible_cause": get_sources(
        cause_final
    ),
    "recommended_action": get_sources(
        action_final
    ),
}


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
- If multiple causes are supported and the report does not distinguish between them, describe them as possibilities.
- Do not treat raw numeric values as high or low unless the documentation provides the applicable limit.
- If a field is not supported by the documentation, return null.
- Return valid JSON only.
- For every non-null result, return the exact supporting rule identifier from the documentation.
- Examples of valid identifiers are "RULE S-06", "CAUSE C-14", and "ACTION A-05".
- If the result is null, its reference must also be null.

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
    "severity_reference": null,

    "possible_cause": null,
    "possible_cause_reference": null,

    "recommended_action": null,
    "recommended_action_reference": null
}}
"""


response = groq_client.chat.completions.create(
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

print("\nRAW MODEL OUTPUT")
print("=" * 60)
print(raw_output)


try:
    parsed_output = json.loads(
        raw_output
    )

except json.JSONDecodeError:
    raise RuntimeError(
        "The model did not return valid JSON."
    )


final_output = {
    "severity": parsed_output.get("severity"),
    "severity_reference": parsed_output.get("severity_reference"),

    "possible_cause": parsed_output.get("possible_cause"),
    "possible_cause_reference": parsed_output.get(
        "possible_cause_reference"
    ),

    "recommended_action": parsed_output.get(
        "recommended_action"
    ),
    "recommended_action_reference": parsed_output.get(
        "recommended_action_reference"
    ),

    "sources": sources,
}


print("\nFINAL RAG OUTPUT")
print("=" * 60)
print(
    json.dumps(
        final_output,
        indent=2
    )
)