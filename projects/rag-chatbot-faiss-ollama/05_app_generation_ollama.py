import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import requests


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


def generate_with_ollama(question: str, retrieved_chunks: list[str], model_name="llama3.2:3b") -> str:
    context = "\n\n".join([f"Chunk {i+1}: {c}" for i, c in enumerate(retrieved_chunks)])

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not present in the context, say:
"I don't know based on the provided document."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""".strip()

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["response"].strip()


if __name__ == "__main__":
    # Load + chunk
    text = load_text_file("data.txt")
    chunks = chunk_text(text)
    print(f"✅ Chunks created: {len(chunks)}")

    # Embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_texts(model, chunks)
    print(f"✅ Embeddings shape: {embeddings.shape}")

    # FAISS index
    index = build_faiss_index(embeddings)
    print(f"✅ FAISS index size: {index.ntotal}")

    # Ask question
    question = "What is RAG and how does it work?"

    # Retrieve
    top_chunks = retrieve_top_chunks(question, model, index, chunks, k=3)

    # Generate
    print("🤖 Generating answer using Ollama...\n")
    answer = generate_with_ollama(question, top_chunks, model_name="llama3.2:3b")

    print("✅ Final Answer:\n")
    print(answer)
