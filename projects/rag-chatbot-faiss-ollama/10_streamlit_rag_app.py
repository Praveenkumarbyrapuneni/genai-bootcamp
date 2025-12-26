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


def generate_with_ollama(question, retrieved_chunks, model_name="llama3.2:3b"):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.

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

    return result.stdout.strip()


# ---------- Streamlit UI ----------
st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("🧠 RAG Chatbot (FAISS + Ollama)")

@st.cache_resource
def setup_rag():
    text = load_text_file("data.txt")
    chunks = chunk_text(text)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_texts(model, chunks)
    index = build_faiss_index(embeddings)
    return model, index, chunks

model, index, chunks = setup_rag()

query = st.text_input("Ask a question:")

if query:
    results = retrieve_top_chunks(index, model, query, chunks)

    with st.spinner("Thinking..."):
        answer = generate_with_ollama(query, [r[2] for r in results])

    st.subheader("🤖 Answer")
    st.write(answer)

    st.subheader("📚 Sources")
    for i, (idx, score, chunk) in enumerate(results, start=1):
        st.markdown(f"**Source {i} (score={score:.2f})**")
        st.write(chunk)
