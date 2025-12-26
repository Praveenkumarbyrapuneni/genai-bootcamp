import streamlit as st
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import subprocess


# ---------- RAG helper functions ----------
def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def chunk_text(text, chunk_size=200, chunk_overlap=40):
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


def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


def retrieve_top_chunks(index, model, query, chunks, k=3):
    q_emb = embed_texts(model, [query])
    scores, ids = index.search(q_emb, k)

    results = []
    for idx, score in zip(ids[0], scores[0]):
        results.append((int(idx), float(score), chunks[int(idx)]))
    return results


def run_ollama(prompt: str, model_name="llama3.2:3b") -> str:
    result = subprocess.run(
        ["ollama", "run", model_name, prompt],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return f"Ollama error:\n{result.stderr}"
    return result.stdout.strip()


# ---------- Decision: use RAG or General ----------
def should_use_rag(results, min_score=0.20) -> bool:
    """
    If the best chunk similarity score is high enough,
    we assume the docs are relevant and use RAG.
    """
    if not results:
        return False
    best_score = results[0][1]
    return best_score >= min_score


def generate_answer_hybrid(query, rag_chunks, use_rag, ollama_model="llama3.2:3b"):
    if use_rag:
        context = "\n\n".join([f"- {c}" for c in rag_chunks])
        prompt = f"""
You are a helpful assistant.

Use BOTH:
1) The CONTEXT below (my private document)
2) Your own general knowledge

Rules:
- If the context contains relevant info, use it and prefer it.
- If the user asks something not covered by the context, answer using general knowledge.
- If you use something from the context, mention it clearly in the answer.
- Keep the answer clear and helpful.

CONTEXT:
{context}

USER QUESTION:
{query}

FINAL ANSWER:
""".strip()
        return run_ollama(prompt, model_name=ollama_model)

    # General chat only
    prompt = f"""
You are a helpful assistant.
Answer normally using your general knowledge.

USER QUESTION:
{query}

ANSWER:
""".strip()
    return run_ollama(prompt, model_name=ollama_model)


# ---------- Streamlit UI ----------
st.set_page_config(page_title="Hybrid Chatbot", layout="centered")
st.title("🧠 Hybrid Chatbot (RAG + General Knowledge) — FAISS + Ollama")

st.caption("✅ Uses your data.txt when relevant • ✅ Otherwise answers from general knowledge • ✅ Shows sources when RAG is used")

@st.cache_resource
def setup_rag():
    text = load_text_file("data.txt")
    chunks = chunk_text(text)
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_texts(embed_model, chunks)
    index = build_faiss_index(embeddings)
    return embed_model, index, chunks

embed_model, index, chunks = setup_rag()

ollama_model = st.selectbox("Choose Ollama model", ["llama3.2:3b", "llama3.1:8b", "mistral", "phi3"], index=0)
k = st.slider("How many sources (top-k)?", min_value=1, max_value=5, value=3)

query = st.text_input("Ask a question:")

if query:
    results = retrieve_top_chunks(index, embed_model, query, chunks, k=k)
    rag_chunks = [r[2] for r in results]

    use_rag = should_use_rag(results, min_score=0.20)

    with st.spinner("Thinking..."):
        answer = generate_answer_hybrid(query, rag_chunks, use_rag, ollama_model=ollama_model)

    st.subheader("🤖 Answer")
    st.write(answer)

    if use_rag:
        st.subheader("📚 Sources (from your data.txt)")
        for i, (idx, score, chunk) in enumerate(results, start=1):
            st.markdown(f"**Source {i} (score={score:.2f}, chunk_id={idx})**")
            st.write(chunk)
    else:
        st.info("No strong match found in your document, so I answered using general knowledge.")
