# 🚀 GenAI Bootcamp - Full-Stack AI Projects Portfolio

> **Enterprise-grade AI applications showcasing modern cloud architecture, LLM integration, and production deployment skills.**

[![Portfolio](https://img.shields.io/badge/Portfolio-3%20Projects-brightgreen)](https://github.com/Praveenkumarbyrapuneni/genai-bootcamp)
[![Azure](https://img.shields.io/badge/Cloud-Microsoft%20Azure-blue)](https://azure.microsoft.com)
[![Render](https://img.shields.io/badge/Hosting-Render-green)](https://render.com)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT--4-purple)](https://openai.com)

---

## 📂 Repository Structure

```
genai-bootcamp/
├── genai_foundations/          # Learning notes & fundamentals
│   ├── day1_notes.md          # GenAI basics
│   ├── day2_notes.md          # Advanced concepts
│   └── README.md
│
└── projects/                   # Production-ready AI applications
    ├── multi-agent-career-advisor/    # ⭐ Main Project (Full-Stack)
    ├── insurance-risk-analysis/       # Insurance risk ML model
    └── rag-chatbot-faiss-ollama/     # RAG chatbot with local LLM
```

---

## 🎯 Featured Projects

### 1. ⭐ **CareerPath AI - Multi-Agent Career Advisor** (Full-Stack)

**🔗 Live Demo:** [https://icy-grass-0516c410f.6.azurestaticapps.net](https://icy-grass-0516c410f.6.azurestaticapps.net)

A brutally honest AI career advisor powered by OpenAI GPT-4 with multi-agent architecture.

**Tech Stack:**
- **Frontend:** Next.js 15, TypeScript, Tailwind CSS
- **Backend:** FastAPI (Python), OpenAI GPT-4o-mini
- **Cloud:** Azure Static Web Apps (Frontend), Render (Backend)
- **Database:** Azure Cosmos DB, Supabase PostgreSQL
- **Auth:** Supabase OAuth (GitHub/Google)

**Key Features:**
- ✅ AI-powered resume analysis with skill extraction
- ✅ Multi-agent system (4 specialized AI agents)
- ✅ Real-time career readiness scoring (0-100%)
- ✅ Personalized learning roadmaps
- ✅ Chat history with Cosmos DB
- ✅ OAuth authentication
- ✅ 180x performance improvement (2-5 sec responses)

**Technical Highlights:**
- Full-stack development (Next.js + FastAPI)
- Cloud deployment on Microsoft Azure + Render
- Multi-agent AI architecture
- NoSQL database management (Cosmos DB)
- Secure authentication (OAuth 2.0)
- File upload & parsing (PDF/DOCX)
- RESTful API design
- Production-ready with CORS, validation, error handling

**📖 [View Full Documentation →](./projects/multi-agent-career-advisor/README.md)**

---

### 2. **Insurance Risk Analysis**

Machine learning model for predicting insurance risk categories.

**Tech Stack:** Python, scikit-learn, pandas  
**Focus:** Data preprocessing, ML model training, evaluation

**📖 [View Project →](./projects/insurance-risk-analysis/)**

---

### 3. **RAG Chatbot with FAISS & Ollama**

Retrieval-Augmented Generation chatbot using local LLM.

**Tech Stack:** Python, FAISS, Ollama, Streamlit  
**Focus:** Vector embeddings, semantic search, local LLM deployment

**Key Components:**
- Document chunking & embeddings
- FAISS vector indexing
- Top-K retrieval
- Local LLM generation (Ollama)
- Streamlit UI with chat memory
- RAG with citations
- Retrieval precision evaluation

**📖 [View Project →](./projects/rag-chatbot-faiss-ollama/)**

---

## 💡 Technical Skills Demonstrated

### **Full-Stack Development**
- ✅ **Frontend:** Next.js 15, React, TypeScript, Tailwind CSS
- ✅ **Backend:** FastAPI, Python, async/await, Uvicorn
- ✅ **APIs:** RESTful design, CORS, validation, error handling
- ✅ **File Handling:** PDF/DOCX parsing, FormData, uploads

### **Cloud & DevOps**
- ✅ **Microsoft Azure:** Static Web Apps, Cosmos DB, Azure CLI
- ✅ **Render.com:** Backend API deployment, environment management
- ✅ **Git/GitHub:** Version control, proper commit history
- ✅ **Environment Management:** Dev vs Production configs

### **AI/ML Integration**
- ✅ **OpenAI GPT-4:** API integration, prompt engineering
- ✅ **Multi-Agent Systems:** Specialized agent architecture
- ✅ **RAG (Retrieval-Augmented Generation):** Vector search, embeddings
- ✅ **Local LLMs:** Ollama integration
- ✅ **Context Management:** Passing data to AI models

### **Database & Storage**
- ✅ **Azure Cosmos DB:** NoSQL database, CRUD operations
- ✅ **Supabase PostgreSQL:** Auth, analytics, RLS
- ✅ **Vector Databases:** FAISS for semantic search
- ✅ **Data Modeling:** User history, analytics tracking

### **Security**
- ✅ **OAuth 2.0:** GitHub & Google authentication
- ✅ **Environment Variables:** Secure credential management
- ✅ **CORS Policies:** Cross-origin security
- ✅ **Input Validation:** Pydantic models, sanitization
- ✅ **Row Level Security:** Supabase RLS policies

---

## 🏗️ Production Architecture (CareerPath AI)

```
User Browser
    ↓
Microsoft Azure Static Web Apps (Frontend - Global CDN)
    ↓ HTTPS/TLS
Render.com (FastAPI Backend)
    ↓
├── OpenAI GPT-4o-mini API (2-5 sec responses)
├── Azure Cosmos DB (NoSQL - Career Data)
└── Supabase PostgreSQL (Auth + Analytics)
```

**Why This Architecture:**
- ✅ **Azure Static Web Apps** - Enterprise CDN, instant global delivery
- ✅ **Render** - Reliable Python hosting, better than Azure free tier
- ✅ **OpenAI GPT-4** - Industry-standard AI, 180x faster than Azure OpenAI
- ✅ **Separation of Concerns** - Frontend/Backend decoupling
- ✅ **Cost-Effective** - Free tiers + optimized API usage

---

## 📈 Performance Metrics (CareerPath AI)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **First Response** | 15+ minutes | 2-5 seconds | **180x faster** |
| **API Cost** | $0.15/1M tokens | **FREE tier** | **100% savings** |
| **Reliability** | Frequent crashes | Stable ✅ | **Much better** |
| **Rate Limit** | Limited | 14,400/day | **Higher capacity** |

---

## 🎓 Learning Journey

### **GenAI Foundations**
- Day 1: Introduction to Generative AI, LLMs, prompt engineering
- Day 2: Advanced prompting, RAG, vector databases  
**[View Learning Notes →](./genai_foundations/)**

### **Project Evolution**
1. **Started with:** Basic RAG chatbot (FAISS + Ollama)
2. **Progressed to:** Full-stack AI app with cloud deployment
3. **Mastered:** Multi-agent systems, production deployment, auth

---

## 💼 Resume Talking Points

### **Project Description:**
> "Built a full-stack AI career advisor using **Next.js 15** and **FastAPI**, deployed on **Microsoft Azure** and **Render**, integrating **OpenAI GPT-4** with a **multi-agent architecture** for specialized career guidance."

### **Technical Achievement:**
> "Optimized AI response times from 15+ minutes to 2-5 seconds by migrating from Azure OpenAI to OpenAI GPT-4o-mini, achieving **180x performance improvement** while reducing costs to zero."

### **Cloud Infrastructure:**
> "Deployed production-grade application on **Microsoft Azure Static Web Apps** (frontend CDN), **Render** (backend API), with **Azure Cosmos DB** for NoSQL storage and **Supabase** for OAuth authentication."

### **System Design:**
> "Implemented multi-agent AI architecture with 4 specialized agents (Career Advisor, Market Researcher, Skills Coach, Application Strategist) coordinated through a central orchestrator pattern."

---

## 🚀 Quick Start

### **Clone Repository:**
```bash
git clone https://github.com/Praveenkumarbyrapuneni/genai-bootcamp.git
cd genai-bootcamp
```

### **Run CareerPath AI Locally:**
```bash
# Backend
cd projects/multi-agent-career-advisor
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

**Full setup instructions:** [projects/multi-agent-career-advisor/README.md](./projects/multi-agent-career-advisor/README.md)

---

## 🎯 Interview Questions I Can Answer

1. **"Tell me about your most complex project"**
   - CareerPath AI: Full-stack, multi-agent, cloud-deployed...

2. **"How did you handle authentication?"**
   - Supabase OAuth 2.0 with GitHub/Google login...

3. **"Describe your cloud deployment strategy"**
   - Azure Static Web Apps for frontend CDN, Render for backend...

4. **"How did you improve performance?"**
   - Migrated from Azure OpenAI to OpenAI GPT-4o-mini, 180x faster...

5. **"What security measures did you implement?"**
   - OAuth 2.0, environment variables, CORS, input validation, RLS...

6. **"Explain your multi-agent system"**
   - 4 specialized agents coordinated by main orchestrator...

---

## 📊 Project Stats

- **3 Production-Ready Projects**
- **2 Cloud Platforms** (Azure, Render)
- **4 AI Agents** (Multi-agent architecture)
- **2 Databases** (Cosmos DB, Supabase)
- **180x Performance Improvement**
- **100% Cost Reduction** (vs Azure OpenAI)

---

## 🙏 Technologies Used

### **Cloud & Infrastructure**
- Microsoft Azure (Static Web Apps, Cosmos DB)
- Render.com
- Supabase
- Vercel (alternative frontend)

### **AI/ML**
- OpenAI GPT-4o-mini
- FAISS (vector search)
- Ollama (local LLM)
- LangChain (RAG)

### **Frontend**
- Next.js 15 (React 19)
- TypeScript
- Tailwind CSS
- App Router

### **Backend**
- FastAPI
- Python 3.11+
- Uvicorn
- Pydantic

### **Databases**
- Azure Cosmos DB (NoSQL)
- Supabase PostgreSQL
- FAISS (vector DB)

---

## 👨‍💻 Author

**Praveen Kumar Byrapuneni**

- 🌐 **Live Demo:** [CareerPath AI](https://icy-grass-0516c410f.6.azurestaticapps.net)
- 💼 **GitHub:** [Praveenkumarbyrapuneni](https://github.com/Praveenkumarbyrapuneni)
- 📧 **Email:** [Your Email]

---

## 📄 License

MIT License - Feel free to use these projects for learning and portfolio purposes!

---

## 🗺️ Roadmap

- [ ] Add frontend deployment to Vercel
- [ ] Implement vector database for resume storage
- [ ] Add real-time job scraping
- [ ] Create mobile app version
- [ ] Add more AI agents (Interview Coach, Salary Negotiator)

---

**Built with ❤️ and cutting-edge AI** 💪  
**Powered by Microsoft Azure, Render, OpenAI GPT-4, and Supabase** ☁️🚀
