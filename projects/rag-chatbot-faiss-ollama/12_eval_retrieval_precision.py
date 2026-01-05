import json
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


# ----------------------------
# Core RAG components (reuse)
# ----------------------------
def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def chunk_text(text: str, chunk_size=200, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


def embed_texts(model, texts):
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings.astype("float32")


def build_faiss_index(embeddings: np.ndarray):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product works with normalized embeddings
    index.add(embeddings)
    return index


def retrieve_top_chunks(index, model, query: str, chunks, k=3):
    query_embedding = embed_texts(model, [query])
    scores, indices = index.search(query_embedding, k)
    return [chunks[idx] for idx in indices[0]]


# ----------------------------
# Evaluation helpers
# ----------------------------
def load_eval_set(path: str):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def precision_at_k(eval_items, index, embed_model, chunks, k: int):
    hits = 0
    missed = []

    for item in eval_items:
        q = item["question"]
        gold_phrase = item["gold_contains"].lower()

        retrieved = retrieve_top_chunks(index, embed_model, q, chunks, k=k)
        retrieved_lc = [r.lower() for r in retrieved]

        hit = any(gold_phrase in r for r in retrieved_lc)
        hits += 1 if hit else 0

        if not hit:
            missed.append(item["id"])

        print(f"[{item['id']}] hit={hit} | k={k} | question={q}")

    precision = hits / max(len(eval_items), 1)
    return precision, hits, missed


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    # Load corpus
    text = load_text_file("data.txt")

    # Load eval set
    eval_items = load_eval_set("eval_set.jsonl")

    # Test multiple chunking configurations
    configs = [
        (150, 20),
        (200, 40),
        (300, 60),
    ]

    for chunk_size, chunk_overlap in configs:
        print("\n" + "=" * 70)
        print(f"=== Config: chunk_size={chunk_size}, overlap={chunk_overlap} ===")

        # Chunk + embed + index
        chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = embed_texts(embed_model, chunks)
        index = build_faiss_index(embeddings)

        print(f"Chunks: {len(chunks)} | Index size: {index.ntotal}")

        for k in [3, 5]:
            p, hits, missed = precision_at_k(eval_items, index, embed_model, chunks, k=k)
            print(f"\nprecision@{k}: {p:.2f} ({hits}/{len(eval_items)})")
            print(f"missed@{k}: {missed}\n")
