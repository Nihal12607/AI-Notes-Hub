import os
import gc
import streamlit as st

# 1. DISABLE CHROMADB TELEMETRY NETWORK CALLS IMMEDIATELY
os.environ["ANONYMOUS_TELEMETRY"] = "False"


# 2. Native zero-dependency text splitter
def recursive_split_text(text: str,chunk_size: int = 1000,chunk_overlap: int = 150):
    chunks = []
    step = chunk_size - chunk_overlap

    for start in range(0, len(text), step):
        end = start + chunk_size
        chunks.append(text[start:end].strip())

    return [c for c in chunks if len(c)>200]

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
    """Splits raw text into chunks, embeds them, and saves to ChromaDB in batches."""

    chunks = recursive_split_text(doc_text, chunk_size=6000, chunk_overlap=350)

    if not chunks:
        return None

    chroma_client = get_chroma_client()

    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = chroma_client.create_collection(name=collection_name)
    
    # Process chunks in batches of 50 to avoid OOM crashes on Streamlit Free Tier
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i : i + batch_size]
        batch_embeddings = get_embeddings(batch_chunks)
        batch_ids = [f"chunk_{j}" for j in range(i, i + len(batch_chunks))]

        collection.add(ids=batch_ids, embeddings=batch_embeddings, documents=batch_chunks)
        
        # Explicitly free up memory after every batch
        del batch_chunks, batch_embeddings, batch_ids
        gc.collect()

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