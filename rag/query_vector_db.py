from pathlib import Path

import chromadb

PROJECT_ROOT = Path(__file__).resolve().parent.parent

client = chromadb.PersistentClient(
    path=str(PROJECT_ROOT / "chroma_db")
)

collection = client.get_collection(
    name="production_knowledge"
)


def retrieve(input_text, document_type, n_results=3):
    results = collection.query(
        query_texts=[input_text],
        n_results=n_results,
        where={
            "document_type": document_type
        }
    )

    return results


def keyword_match(document_type, keyword):
    stored = collection.get(
        where={"document_type": document_type},
        include=["documents", "metadatas"]
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

def merge_results(
    semantic_documents,
    semantic_metadatas,
    keyword_results
):
    merged = []
    seen = set()

    for item in keyword_results:
        document = item["document"]
        metadata = item["metadata"]

        if document not in seen:
            merged.append(
                {
                    "document": document,
                    "metadata": metadata
                }
            )
            seen.add(document)

    for document, metadata in zip(
        semantic_documents,
        semantic_metadatas
    ):
        if document.startswith("SOURCE NOTE"):
            continue

        if document.startswith("DOCUMENT_TYPE"):
            continue

        if document not in seen:
            merged.append(
                {
                    "document": document,
                    "metadata": metadata
                }
            )
            seen.add(document)

    return merged[:3]

input_text = """
Problem Type: Quality
Problem Description: The molded part has a short shot and is not completely filled.
Downtime: 10
Temperature: 220
Pressure: 120
Cycle Time: 42
Operator Comment: The cavity is not filling completely.
"""

detected_keyword = detect_issue_keyword(input_text)

print("\nDetected keyword:", detected_keyword)
cause_query = "flash around the mold parting line"


for document_type in ["severity", "cause", "action"]:

    print("\n" + "=" * 60)
    print(f"DOCUMENT TYPE: {document_type.upper()}")
    print("=" * 60)

    if document_type == "cause":
        query_text = cause_query
        current_n_results = 10
    else:
        query_text = input_text
        current_n_results = 3

    results = retrieve(
        input_text=query_text,
        document_type=document_type,
        n_results=current_n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for index, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1
    ):
        print(f"\nResult {index}")
        print(f"Source: {metadata['source']}")
        print(f"Type: {metadata['document_type']}")
        print(f"Source type: {metadata.get('source_type')}")
        print(f"Priority: {metadata.get('priority')}")
        print(document)

    if document_type == "cause":
        keyword_results = []

        if detected_keyword:
            keyword_results = keyword_match(
                document_type="cause",
                keyword=detected_keyword
            )

        final_results = merge_results(
            documents,
            metadatas,
            keyword_results
        )

        print("\n" + "-" * 60)
        print("FINAL HYBRID RESULTS")
        print("-" * 60)

        for index, item in enumerate(
                final_results,
                start=1
        ):
            print(f"\nFinal Result {index}")
            print(f"Source: {item['metadata']['source']}")
            print(item["document"])

        print("\n" + "-" * 60)
        print("KEYWORD MATCHES")
        print("-" * 60)

        for index, item in enumerate(
            keyword_results,
            start=1
        ):
            print(f"\nKeyword Result {index}")
            print(f"Source: {item['metadata']['source']}")
            print(f"Type: {item['metadata']['document_type']}")
            print(f"Source type: {item['metadata'].get('source_type')}")
            print(f"Priority: {item['metadata'].get('priority')}")
            print(item["document"])