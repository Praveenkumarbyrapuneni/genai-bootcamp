# 🤖 RAG Chatbot using FAISS + Ollama

A fully local **Retrieval-Augmented Generation (RAG)** chatbot built step-by-step using **FAISS**, **Sentence Transformers**, **Ollama (LLaMA)**, and **Streamlit**.  
This project demonstrates a complete GenAI pipeline — from document ingestion to a production-ready chat UI — with hybrid intelligence (private documents + general LLM knowledge).

---

## 🚀 Project Overview

This chatbot answers user questions by:
- Using **your own documents** when relevant (RAG)
- Falling back to **general LLM knowledge** when documents don’t contain the answer
- Showing **source citations** whenever document-based answers are used

Everything runs **locally**. No paid APIs.

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)** improves LLM answers by grounding them in external documents.

Flow:
User Question → Embedding → FAISS Vector Search → Relevant Chunks → LLM → Final Answer

---

## ✨ Key Features

- Local document ingestion (`data.txt`)
- Text chunking with overlap
- Embeddings using `all-MiniLM-L6-v2`
- FAISS vector similarity search
- Local LLM inference with Ollama (LLaMA)
- Hybrid answers (RAG + general knowledge)
- Source citations
- Conversational memory
- Streamlit interactive UI
- Modular learning-friendly file structure

---

## 📁 Project Structure

rag-chatbot-faiss-ollama/
├── data.txt
├── 01_app_chunks.py
├── 02_app_embeddings.py
├── 03_app_faiss_indexing.py
├── 04_app_top_chunks_retrieval.py
├── 05_app_generation_ollama.py
├── 06_app_pipeline_fixed_questions.py
├── 07_RAG_loop_app.py
├── 08_rag_with_citations_app.py
├── 09_rag_with_memory_app.py
├── 10_streamlit_rag_app.py
├── 11_streamlit_rag_plus_general_chat_app.py
└── README.md


---

## 🛠️ Tech Stack

- Python
- FAISS
- Sentence Transformers
- Ollama (LLaMA models)
- Streamlit
- LangChain Text Splitters

---

## ⚙️ Setup Instructions

Create virtual environment:
python -m venv rag-env
source rag-env/bin/activate


Install dependencies:
pip install faiss-cpu sentence-transformers langchain streamlit


Install Ollama and model:
brew install ollama
ollama pull llama3.2:3b


---

## ▶️ How to Run

Run CLI RAG loop:
python 07_RAG_loop_app.py


Run Streamlit UI:
streamlit run 11_streamlit_rag_plus_general_chat_app.py

Open browser:
http://localhost:8501


---

## 🧪 Example Behavior

- If the answer exists in `data.txt` → uses retrieved chunks + shows sources
- If not → answers from general LLM knowledge (no fake citations)

---

## 🎯 Learning Outcomes

- Built an end-to-end RAG system
- Learned embeddings and vector databases
- Implemented FAISS similarity search
- Controlled hallucinations
- Deployed local LLMs using Ollama
- Built a GenAI web app using Streamlit
- Structured a real-world GenAI project

---

## 🚧 Future Improvements

- PDF / multi-file ingestion
- Persistent FAISS index
- User authentication
- Docker deployment
- Cloud vector DB support

---

## 👤 Author

**Praveen Kumar Byrapuneni**  
GenAI Bootcamp Participant  

GitHub: https://github.com/Praveenkumarbyrapuneni

---

⭐ If you found this project useful, please star the repository!
