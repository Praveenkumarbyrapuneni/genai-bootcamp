from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np


def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def chunk_text(text: str, chunk_size=200, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


def embed_texts(model, texts):
    # returns numpy array shape: (num_texts, embedding_dim)
    emb = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return emb.astype("float32")


if __name__ == "__main__":
    # 1) Load + chunk
    text = load_text_file("data.txt")
    chunks = chunk_text(text)
    print(f"✅ Total chunks created: {len(chunks)}")

    # 2) Embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_embeddings = embed_texts(model, chunks)

    print("✅ Embeddings created!")
    print(f"Embedding matrix shape: {chunk_embeddings.shape}")  # (chunks, 384)
    print(f"First embedding (first 10 numbers): {chunk_embeddings[0][:10]}")
