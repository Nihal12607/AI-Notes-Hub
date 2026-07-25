import os
import streamlit as st

# 1. DISABLE CHROMADB TELEMETRY NETWORK CALLS IMMEDIATELY
os.environ["ANONYMOUS_TELEMETRY"] = "False"


# 2. Native zero-dependency text splitter (Replaces heavy langchain import)
def recursive_split_text(
    text: str, chunk_size: int = 1000, chunk_overlap: int = 150
) -> list[str]:
    """Pure Python text splitter with zero library dependencies."""
    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        if end >= text_length:
            chunks.append(text[start:].strip())
            break

        # Try splitting on natural paragraph or sentence boundaries
        split_pos = -1
        for sep in ["\n\n", "\n", ". ", " "]:
            pos = text.rfind(sep, start, end)
            if pos != -1 and pos > start:
                split_pos = pos + len(sep)
                break

        if split_pos == -1:
            split_pos = end

        chunks.append(text[start:split_pos].strip())
        start = max(start + 1, split_pos - chunk_overlap)

    return [c for c in chunks if c]


# 3. Lazy-load ChromaDB inside cache wrapper
@st.cache_resource(show_spinner=False)
def get_chroma_client():
    import chromadb
    from chromadb.config import Settings

    return chromadb.Client(Settings(anonymized_telemetry=False))


# 4. Lazy-load FastEmbed inside cache wrapper
@st.cache_resource(show_spinner=False)
def load_embedder():
    from fastembed import TextEmbedding

    return TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


def get_embeddings(texts: list[str]) -> list[list[float]]:
    embedder = load_embedder()
    embeddings = list(embedder.embed(texts))
    return [e.tolist() for e in embeddings]


def index_document(doc_text: str, collection_name: str = "user_pdf"):
    """Splits raw text into chunks, embeds them, and saves to ChromaDB."""
    chunks = recursive_split_text(doc_text, chunk_size=1000, chunk_overlap=150)

    if not chunks:
        return None

    chroma_client = get_chroma_client()

    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = chroma_client.create_collection(name=collection_name)
    embeddings = get_embeddings(chunks)
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(ids=ids, embeddings=embeddings, documents=chunks)
    return collection


def retrieve_context(
    query: str, collection_name: str = "user_pdf", top_k: int = 4
) -> str:
    """Finds top_k relevant chunks for user prompt."""
    try:
        chroma_client = get_chroma_client()
        collection = chroma_client.get_collection(name=collection_name)
    except Exception:
        return ""

    count = collection.count()
    if count == 0:
        return ""

    query_embeddings = get_embeddings([query])
    results = collection.query(
        query_embeddings=query_embeddings, n_results=min(top_k, count)
    )

    if results and "documents" in results and results["documents"]:
        retrieved_chunks = results["documents"][0]
        return "\n\n--- CONTEXT SEPARATOR ---\n\n".join(retrieved_chunks)
    return ""