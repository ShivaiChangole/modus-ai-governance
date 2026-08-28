import os
import chromadb
from chromadb.utils import embedding_functions

# Initialize persistent ChromaDB instance
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
client = chromadb.PersistentClient(path=DB_DIR)

# Use free local Sentence Transformer embeddings
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="ai_governance_rules",
    embedding_function=embedding_fn
)

# Seed documents across required regulatory tiers
governance_docs = [
    {
        "id": "gov_001",
        "text": "High-risk AI systems deployed in critical infrastructure, healthcare, or employment evaluation must conduct comprehensive bias auditing, risk assessments, and maintain continuous human oversight under Article 14.",
        "source": "EU AI Act - Article 14",
        "source_type": "Law / Regulation",
        "jurisdiction": "EU",
        "category": "Human Oversight & Risk"
    },
    {
        "id": "gov_002",
        "text": "Organizations processing personally identifiable information (PII) or medical records for model training must implement strict differential privacy, encryption at rest, and zero-data retention policies.",
        "source": "HIPAA / GDPR Data Privacy Framework",
        "source_type": "Law / Regulation",
        "jurisdiction": "Global",
        "category": "Data Privacy"
    },
    {
        "id": "gov_003",
        "text": "NIST AI Risk Management Framework (AI RMF 1.0) recommends mapping system boundaries, establishing explainability metrics for black-box models, and maintaining incident log repositories.",
        "source": "NIST AI RMF 1.0",
        "source_type": "Regulatory Guidance",
        "jurisdiction": "US",
        "category": "Explainability & Governance"
    },
    {
        "id": "gov_004",
        "text": "ISO/IEC 42001 specifies requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) within organizations.",
        "source": "ISO/IEC 42001:2023",
        "source_type": "Industry Standard",
        "jurisdiction": "International",
        "category": "Management System"
    },
    {
        "id": "gov_005",
        "text": "Automated financial lending or credit scoring AI systems require statistical parity and disparate impact checks across demographic classes to prevent algorithmic discrimination.",
        "source": "FTC Consumer Protection AI Guidance",
        "source_type": "Regulatory Guidance",
        "jurisdiction": "US",
        "category": "Bias/Fairness"
    }
]

# Ingest into vector store
documents = [doc["text"] for doc in governance_docs]
metadatas = [
    {
        "source": doc["source"],
        "source_type": doc["source_type"],
        "jurisdiction": doc["jurisdiction"],
        "category": doc["category"]
    }
    for doc in governance_docs
]
ids = [doc["id"] for doc in governance_docs]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Successfully ingested {len(ids)} governance records into local ChromaDB!")
