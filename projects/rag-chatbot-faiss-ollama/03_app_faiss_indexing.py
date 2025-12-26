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
    # (num_texts, embedding_dim)
    emb = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return emb.astype("float32")


def build_faiss_index(embeddings: np.ndarray):
    dim = embeddings.shape[1]          # 384 for all-MiniLM-L6-v2
    index = faiss.IndexFlatIP(dim)     # Inner Product (good with normalized vectors)
    index.add(embeddings)              # store vectors
    return index


def search(index, model, query: str, chunks: list[str], k: int = 3):
    q_emb = embed_texts(model, [query])        # (1, dim)
    scores, ids = index.search(q_emb, k)       # (1,k), (1,k)

    print("\n🔎 Query:", query)
    print("Top matches:\n")

    for rank, (idx, score) in enumerate(zip(ids[0], scores[0]), start=1):
        print(f"--- Match {rank} | score={score:.4f} | chunk_id={idx} ---")
        print(chunks[idx])
        print()


if __name__ == "__main__":
    # 1) Load + chunk
    text = load_text_file("data.txt")
    chunks = chunk_text(text)
    print(f"✅ Total chunks created: {len(chunks)}")

    # 2) Embed chunks
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_embeddings = embed_texts(model, chunks)
    print(f"✅ Embeddings shape: {chunk_embeddings.shape} (chunks, 384)")

    # 3) Build FAISS index
    index = build_faiss_index(chunk_embeddings)
    print(f"✅ FAISS index size: {index.ntotal} vectors")

    # 4) Test retrieval
    search(index, model, "What is RAG and how does it work?", chunks, k=3)
    search(index, model, "Where do we store embeddings and why?", chunks, k=3)
