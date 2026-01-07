import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import subprocess


# ---------------------------
# 1) Load + Chunk documents
# ---------------------------
def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def chunk_text(text: str, chunk_size=200, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


# ---------------------------
# 2) Embeddings
# ---------------------------
def embed_texts(model, texts):
    # returns numpy array shape: (num_texts, embedding_dim)
    emb = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return emb.astype("float32")


# ---------------------------
# 3) Build FAISS index
# ---------------------------
def build_faiss_index(embeddings: np.ndarray):
    dim = embeddings.shape[1]  # e.g., 384
    index = faiss.IndexFlatIP(dim)  # inner product (best with normalized vectors)
    index.add(embeddings)
    return index


# ---------------------------
# 4) Retrieve top chunks
# ---------------------------
def retrieve_top_chunks(index, model, query: str, chunks: list[str], k: int = 3):
    q_emb = embed_texts(model, [query])  # shape (1, dim)
    scores, ids = index.search(q_emb, k)

    results = []
    for idx, score in zip(ids[0], scores[0]):
        results.append((int(idx), float(score), chunks[int(idx)]))
    return results


# ---------------------------
# 5) Generate answer using Ollama
# ---------------------------
def generate_answer_with_ollama(query: str, retrieved_chunks: list[str], ollama_model="llama3.2:3b"):
    context = "\n\n".join([f"- {c}" for c in retrieved_chunks])

    prompt = f"""
You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say: "I don't know based on the provided documents."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER (clear and short):
""".strip()

    # Call Ollama CLI
    result = subprocess.run(
        ["ollama", "run", ollama_model, prompt],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Ollama error:\n{result.stderr}")

    return result.stdout.strip()


# ---------------------------
# 6) Full RAG Search + Answer
# ---------------------------
def rag_ask(index, embed_model, query: str, chunks: list[str], k: int = 3, ollama_model="llama3.2:3b"):
    results = retrieve_top_chunks(index, embed_model, query, chunks, k=k)

    print("\n🔎 Query:", query)
    print("Top matches:\n")
    retrieved_texts = []
    for rank, (idx, score, chunk_text) in enumerate(results, start=1):
        print(f"--- Match {rank} | score={score:.4f} | chunk_id={idx} ---")
        print(chunk_text)
        print()
        retrieved_texts.append(chunk_text)

    print("🤖 Generating final answer with Ollama...\n")
    answer = generate_answer_with_ollama(query, retrieved_texts, ollama_model=ollama_model)

    print("✅ Final Answer:\n")
    print(answer)
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    # A) Load + chunk
    text = load_text_file("data.txt")
    chunks = chunk_text(text)
    print(f"✅ Total chunks created: {len(chunks)}")

    # B) Embeddings
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_embeddings = embed_texts(embed_model, chunks)
    print(f"✅ Embeddings shape: {chunk_embeddings.shape}  (chunks, 384)")

    # C) Build FAISS index
    index = build_faiss_index(chunk_embeddings)
    print(f"✅ FAISS index size: {index.ntotal} vectors")

    # D) Ask questions (RAG)
    rag_ask(index, embed_model, "What is RAG and how does it work?", chunks, k=3, ollama_model="llama3.2:3b")
    rag_ask(index, embed_model, "Where do we store embeddings and why?", chunks, k=3, ollama_model="llama3.2:3b")
