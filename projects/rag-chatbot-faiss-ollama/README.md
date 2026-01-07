# Production-Style RAG System (FAISS + Ollama)

This project implements a Retrieval-Augmented Generation (RAG) system with
evaluation, hallucination prevention, and cost-aware design.

## Architecture Overview
- Document chunking using RecursiveCharacterTextSplitter
- Sentence embeddings via sentence-transformers
- Vector search using FAISS (cosine similarity)
- Local LLM inference using Ollama
- Streamlit-based interactive UI

## Retrieval Evaluation
- Implemented precision@k evaluation on a labeled question set
- Tested multiple chunking configurations
- Achieved 100% precision@5 on the evaluation dataset

## Hallucination Prevention
- Added confidence-aware routing using similarity score thresholds
- Automatically disables RAG and falls back to general chat when retrieval confidence is low
- Prevents unsupported or hallucinated answers

## Cost & Scaling Considerations
- Default setup uses local FAISS + Ollama to avoid per-request LLM API costs during development
- Retrieval and generation layers are decoupled, allowing migration to hosted LLM APIs for multi-user production scaling

## How to Run
```bash
streamlit run 11_streamlit_rag_plus_general_chat_app.py
