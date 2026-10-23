
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DOCUMENT_PATH = PROJECT_ROOT / "knowledge_base" / "support_faq.txt"
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

COLLECTION_NAME = "support_knowledge"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    return _embedding_model

def load_documents() -> str:
    """Read the support knowledge base."""
    if not DOCUMENT_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {DOCUMENT_PATH}"
        )

    return DOCUMENT_PATH.read_text(encoding="utf-8")


def chunk_document(text: str) -> list[str]:
    """Split the document into sections using its headings."""
    sections = text.split("\n## ")
    chunks = []

    for section in sections:
        section = section.strip()
        if section:
            chunks.append(section)

    return chunks


def build_knowledge_base():
    """Embed document chunks and store them in ChromaDB."""
    document_text = load_documents()
    chunks = chunk_document(document_text)

    if not chunks:
        raise ValueError("No document chunks were created.")

    model = get_embedding_model()

    embeddings = model.encode(chunks).tolist()

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    # Rebuild this collection each time the ingestion script runs.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[f"support-{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {"source": DOCUMENT_PATH.name, "chunk": i}
            for i in range(len(chunks))
        ],
    )

    print(f"Indexed {len(chunks)} chunks.")
    print(f"ChromaDB location: {CHROMA_PATH}")


def search_knowledge_base(query: str, top_k: int = 2) -> list[str]:
    """Return the most relevant support document chunks."""
    if not query.strip():
        return []

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    collection = client.get_collection(COLLECTION_NAME)
    model = get_embedding_model()

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
    )

    return results["documents"][0] if results["documents"] else []

def ensure_knowledge_base():
    """Build the knowledge base if it doesn't exist yet."""
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

    try:
        collection = client.get_collection(COLLECTION_NAME)

        if collection.count() > 0:
            print("Knowledge base already initialized.")
            return

    except Exception:
        pass

    print("Initializing support knowledge base...")
    build_knowledge_base()