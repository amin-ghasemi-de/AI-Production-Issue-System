from pathlib import Path

import chromadb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

DOCUMENTS = {
    "severity_rules.txt": {
        "document_type": "severity",
        "source_type": "external",
        "priority": 4,
    },
    "cause_reference.txt": {
        "document_type": "cause",
        "source_type": "external",
        "priority": 4,
    },
    "recommended_actions.txt": {
        "document_type": "action",
        "source_type": "external",
        "priority": 4,
    },
}

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection_name = "production_knowledge"

try:
    client.delete_collection(collection_name)
except Exception:
    pass

collection = client.create_collection(
    name=collection_name
)

all_documents = []
all_metadatas = []
all_ids = []

for filename, document_info in DOCUMENTS.items():
    document_type = document_info["document_type"]
    source_type = document_info["source_type"]
    priority = document_info["priority"]
    file_path = KNOWLEDGE_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {file_path}"
        )

    text = file_path.read_text(
        encoding="utf-8"
    )

    chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    for index, chunk in enumerate(chunks):
        all_documents.append(chunk)

        all_metadatas.append(
            {
                "source": filename,
                "document_type": document_type,
                "source_type": source_type,
                "priority": priority,
                "chunk_index": index,
            }
        )

        all_ids.append(
            f"{document_type}_{index}"
        )

collection.add(
    documents=all_documents,
    metadatas=all_metadatas,
    ids=all_ids,
)

print(
    f"Added {len(all_documents)} chunks to ChromaDB"
)

for document_info in DOCUMENTS.values():
    document_type = document_info["document_type"]

    count = sum(
        1
        for metadata in all_metadatas
        if metadata["document_type"] == document_type
    )

    print(
        f"{document_type}: {count} chunks"
    )