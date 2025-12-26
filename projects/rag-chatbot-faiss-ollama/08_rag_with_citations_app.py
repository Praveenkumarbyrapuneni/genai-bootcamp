import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import subprocess


# -------------------------------------------------
# 1) Load document
# -------------------------------------------------
def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


# -------------------------------------------------
# 2) Chunk document
# -------------------------------------------------
def chunk_text(text: str, chunk_size=200, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


# -------------------------------------------------
# 3) Create embeddings
# -------------------------------------------------
def embed_texts(model, texts):
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings.astype("float32")


# -------------------------------------------------
# 4) Build FAISS index
# -------------------------------------------------
def build_faiss_index(embeddings: np.ndarray):
    dim = embeddings.shape[1]          # 384 for all-MiniLM-L6-v2
    index = faiss.IndexFlatIP(dim)     # inner product (works like cosine if vectors are normalized)
    index.add(embeddings)
    return index


# -------------------------------------------------
# 5) Retrieve top chunks (now returns citations too)
# -------------------------------------------------
def retrieve_top_chunks(index, model, query: str, chunks, k=3):
    query_embedding = embed_texts(model, [query])     # (1, dim)
    scores, indices = index.search(query_embedding, k)

    # Build list of: (chunk_id, score, chunk_text)
    results = []
    for answer_rank, (idx, score) in enumerate(zip(indices[0], scores[0]), start=1):
        idx = int(idx)
        score = float(score)
        results.append((idx, score, chunks[idx]))
    return results


# -------------------------------------------------
# 6) Generate answer using Ollama
# -------------------------------------------------
def generate_answer_with_ollama(question: str, retrieved_chunks, model_name="llama3.2:3b"):
    context = "\n\n".join([f"[Source {i+1}] {c}" for i, c in enumerate(retrieved_chunks)])

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say:
"I don't know based on the provided documents."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER (clear and short):
""".strip()

    result = subprocess.run(
        ["ollama", "run", model_name, prompt],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()


# -------------------------------------------------
# 7) RAG pipeline (prints citations at the end)
# -------------------------------------------------
def rag_answer(index, embed_model, query, chunks, k=3, ollama_model="llama3.2:3b"):
    results = retrieve_top_chunks(index, embed_model, query, chunks, k=k)

    print("\n🔎 User Question:", query)
    print("📌 Retrieved chunks:\n")

    retrieved_texts = []
    for rank, (chunk_id, score, chunk_text_value) in enumerate(results, start=1):
        print(f"--- Rank {rank} | score={score:.4f} | chunk_id={chunk_id} ---")
        print(chunk_text_value)
        print()
        retrieved_texts.append(chunk_text_value)

    print("🤖 Generating answer with Ollama...\n")
    answer = generate_answer_with_ollama(query, retrieved_texts, model_name=ollama_model)

    print("✅ Final Answer:\n")
    print(answer)

    # ---- CITATIONS / SOURCES ----
    print("\n📚 Sources used (citations):")
    for rank, (chunk_id, score, chunk_text_value) in enumerate(results, start=1):
        preview = chunk_text_value.replace("\n", " ")
        if len(preview) > 90:
            preview = preview[:90] + "..."
        print(f"[{rank}] chunk_id={chunk_id}, score={score:.4f} | {preview}")

    print("\n" + "=" * 60 + "\n")


# -------------------------------------------------
# MAIN: Interactive loop
# -------------------------------------------------
if __name__ == "__main__":
    print("🚀 Building RAG system...\n")

    # Load + chunk
    text = load_text_file("data.txt")
    chunks = chunk_text(text)
    print(f"✅ Total chunks created: {len(chunks)}")

    # Embeddings
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_texts(embed_model, chunks)
    print(f"✅ Embeddings shape: {embeddings.shape} (chunks, 384)")

    # FAISS index
    index = build_faiss_index(embeddings)
    print(f"✅ FAISS index size: {index.ntotal}")

    # Interactive loop
    print("\n🧠 RAG is ready!")
    print("Type your question below (type 'exit' to quit)\n")

    while True:
        query = input("🧑 You: ").strip()

        if query.lower() in {"exit", "quit", "q"}:
            print("👋 Exiting RAG. Bye!")
            break

        if not query:
            continue

        rag_answer(index, embed_model, query, chunks, k=3, ollama_model="llama3.2:3b")
