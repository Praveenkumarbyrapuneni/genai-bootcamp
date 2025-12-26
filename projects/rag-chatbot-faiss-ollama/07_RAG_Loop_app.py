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
    dim = embeddings.shape[1]  # 384
    index = faiss.IndexFlatIP(dim)  # cosine similarity (normalized)
    index.add(embeddings)
    return index


# -------------------------------------------------
# 5) Retrieve top chunks
# -------------------------------------------------
def retrieve_top_chunks(index, model, query: str, chunks, k=3):
    query_embedding = embed_texts(model, [query])
    scores, indices = index.search(query_embedding, k)

    retrieved_chunks = []
    print("\n🔎 Retrieved chunks:\n")

    for rank, (idx, score) in enumerate(zip(indices[0], scores[0]), start=1):
        print(f"--- Rank {rank} | score={score:.4f} ---")
        print(chunks[idx])
        print()
        retrieved_chunks.append(chunks[idx])

    return retrieved_chunks


# -------------------------------------------------
# 6) Generate answer using Ollama
# -------------------------------------------------
def generate_answer_with_ollama(question: str, retrieved_chunks, model_name="llama3.2:3b"):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say:
"I don't know based on the provided documents."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
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
# 7) RAG pipeline
# -------------------------------------------------
def rag_answer(index, embed_model, query, chunks, k=3):
    retrieved_chunks = retrieve_top_chunks(index, embed_model, query, chunks, k)
    print("🤖 Generating answer with Ollama...\n")
    answer = generate_answer_with_ollama(query, retrieved_chunks)
    print("✅ Final Answer:\n")
    print(answer)
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

    # Interactive Q&A loop
    print("\n🧠 RAG is ready!")
    print("Type your question below (type 'exit' to quit)\n")

    while True:
        query = input("🧑 You: ").strip()

        if query.lower() in {"exit", "quit", "q"}:
            print("👋 Exiting RAG. Bye!")
            break

        if not query:
            continue

        rag_answer(index, embed_model, query, chunks, k=3)
