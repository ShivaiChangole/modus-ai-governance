import os
import chromadb
from chromadb.utils import embedding_functions

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")

def get_chroma_collection():
    client = chromadb.PersistentClient(path=DB_DIR)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(
        name="ai_governance_rules",
        embedding_function=embedding_fn
    )

def query_governance_rules(query_text: str, n_results: int = 3):
    collection = get_chroma_collection()
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    citations = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0] if "distances" in results else []
        
        for idx, doc in enumerate(docs):
            meta = metas[idx]
            citations.append({
                "content": doc,
                "source": meta.get("source", "Unknown"),
                "source_type": meta.get("source_type", "General Web Content"),
                "category": meta.get("category", "General"),
                "jurisdiction": meta.get("jurisdiction", "Global")
            })
    return citations
