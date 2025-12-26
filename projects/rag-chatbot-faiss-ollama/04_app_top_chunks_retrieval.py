from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def chunk_text(text: str, chunk_size=200, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


def embed_texts(model, texts):
    return model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")


def build_faiss_index(embeddings: np.ndarray):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


def retrieve_top_chunks(query, model, index, chunks, k=3):
    query_embedding = embed_texts(model, [query])
    scores, indices = index.search(query_embedding, k)

    retrieved_chunks = []

    print("\n🔎 User Question:", query)
    print("📌 Retrieved Chunks:\n")

    for rank, (idx, score) in enumerate(zip(indices[0], scores[0]), start=1):
        chunk_text = chunks[idx]
        retrieved_chunks.append(chunk_text)

        print(f"--- Rank {rank} | Score: {score:.4f} ---")
        print(chunk_text)
        print()

    return retrieved_chunks


if __name__ == "__main__":
    # Load document
    text = load_text_file("data.txt")

    # Chunk document
    chunks = chunk_text(text)
    print(f"✅ Chunks created: {len(chunks)}")

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Embed chunks
    embeddings = embed_texts(model, chunks)
    print(f"✅ Embeddings shape: {embeddings.shape}")

    # Build FAISS index
    index = build_faiss_index(embeddings)
    print(f"✅ FAISS index size: {index.ntotal}")

    # Retrieve
    retrieve_top_chunks(
        query="What is RAG and how does it work?",
        model=model,
        index=index,
        chunks=chunks,
        k=3
    )
