# 🚀 Multi-Agent Career Advisor

**AI-Powered Career Guidance Platform Built with Microsoft Semantic Kernel**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0078D4.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![Semantic Kernel](https://img.shields.io/badge/Semantic-Kernel-742774.svg)](https://github.com/microsoft/semantic-kernel)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Key Components](#-key-components)
- [API Endpoints](#-api-endpoints)
- [Setup Instructions](#-setup-instructions)
- [Environment Variables](#-environment-variables)
- [Skills Demonstrated](#-skills-demonstrated)

---

## 🎯 Project Overview

**Multi-Agent Career Advisor** is an intelligent career guidance platform that leverages multiple specialized AI agents to provide personalized career advice, skills analysis, market research, and application strategies.

The system uses **Microsoft Semantic Kernel** to orchestrate multiple AI agents, each with specific expertise, working together to deliver comprehensive career guidance.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Agent AI** | 4 specialized agents working together |
| 📊 **Market Analysis** | Real-time job market trends and insights |
| 🎯 **Skills Analysis** | Personalized gap analysis and learning paths |
| 📝 **Application Strategy** | Resume optimization and interview prep |
| 💾 **Persistent Memory** | Azure Cosmos DB for conversation history |
| 🔐 **Secure Auth** | GitHub/Google OAuth via Supabase |
| ⚡ **Modern Frontend** | Next.js 15 with real-time updates |

---

## 🛠 Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Core programming language |
| **Microsoft Semantic Kernel** | AI orchestration framework |
| **FastAPI** | REST API framework |
| **Azure OpenAI GPT-4o-mini** | Large Language Model |
| **Azure OpenAI text-embedding-ada-002** | Vector embeddings |
| **Azure Cosmos DB** | NoSQL database for persistence |
| **Supabase** | Authentication (GitHub/Google OAuth) |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Next.js 15** | React framework with App Router |
| **TypeScript** | Type-safe JavaScript |
| **Tailwind CSS** | Utility-first CSS styling |
| **Supabase Client** | Authentication management |

### Cloud Services
| Service | Purpose |
|---------|---------|
| **Azure OpenAI Service** | LLM and embeddings API |
| **Azure Cosmos DB** | Persistent data storage |
| **Supabase** | Auth + Real-time database |

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER REQUEST                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NEXT.JS FRONTEND                            │
│                   (React + TypeScript)                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│                    (REST API Layer)                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SEMANTIC KERNEL                               │
│               (AI Orchestration Layer)                           │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│    CAREER     │     │    MARKET     │     │    SKILLS     │
│   ADVISOR     │     │  RESEARCHER   │     │    COACH      │
│    AGENT      │     │    AGENT      │     │    AGENT      │
└───────────────┘     └───────────────┘     └───────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                    ┌───────────────────┐
                    │   APPLICATION     │
                    │   STRATEGIST      │
                    │      AGENT        │
                    └───────────────────┘
                                │
                                ▼
                    ┌───────────────────┐
                    │  AZURE COSMOS DB  │
                    │    (Memory)       │
                    └───────────────────┘
```

### 🤖 Agent Descriptions

| Agent | Role | Capabilities |
|-------|------|--------------|
| **Career Advisor** | Main Orchestrator | Coordinates agents, provides holistic guidance |
| **Market Researcher** | Market Intelligence | Job trends, salary data, industry analysis |
| **Skills Coach** | Skills Development | Gap analysis, learning paths, resources |
| **Application Strategist** | Job Applications | Resume tips, interview prep, networking |

---

## 📁 Project Structure

```
multi-agent-career-advisor/
├── 📂 api/
│   └── main.py                      # FastAPI application
├── 📂 src/
│   ├── kernel_config.py             # Semantic Kernel configuration
│   ├── 📂 agents/
│   │   ├── base_agent.py            # Base agent class
│   │   ├── career_advisor.py        # Career Advisor agent
│   │   ├── market_researcher.py     # Market Researcher agent
│   │   ├── skills_coach.py          # Skills Coach agent
│   │   └── application_strategist.py # Application Strategist
│   ├── 📂 auth/
│   │   ├── supabase_auth.py         # Supabase authentication
│   │   └── oauth_manager.py         # OAuth management
│   ├── 📂 database/
│   │   └── cosmos_manager.py        # Cosmos DB operations
│   ├── 📂 memory/
│   │   └── career_memory.py         # Semantic memory management
│   ├── 📂 planning/
│   │   └── career_planner.py        # Career planning logic
│   └── 📂 plugins/
│       └── job_intelligence/        # Job scraping & analysis
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 app/
│   │   │   ├── page.tsx             # Main page
│   │   │   └── layout.tsx           # App layout
│   │   ├── 📂 components/
│   │   │   ├── Dashboard.tsx        # Main dashboard
│   │   │   └── Login.tsx            # Login component
│   │   └── 📂 lib/
│   │       └── supabase.ts          # Supabase client
│   └── package.json
├── 📂 episodes/                      # Development tutorials
├── 📂 prompts/                       # Prompt templates
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment template
└── README.md                         # This file
```

---

## 🔧 Key Components

### 1. Semantic Kernel Configuration (`kernel_config.py`)
- Initializes Azure OpenAI chat completion service
- Configures text embedding service for semantic memory
- Sets up kernel plugins and memory stores
- Manages API connections and authentication

### 2. Agent System
- **BaseAgent**: Abstract base class with common functionality
- Each agent has specific system prompts and capabilities
- Agents communicate through Semantic Kernel orchestration
- Supports both synchronous and streaming responses

### 3. Memory System
- Uses Azure Cosmos DB for persistent storage
- Semantic memory for context-aware retrieval
- Stores user profiles, conversation history, and career data
- Vector embeddings for similarity search

### 4. Authentication
- Supabase Authentication integration
- Supports GitHub OAuth
- Supports Google OAuth
- JWT token validation
- Secure session management

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Main chat endpoint for career guidance |
| `POST` | `/api/analyze-skills` | Analyzes user skills and identifies gaps |
| `POST` | `/api/market-research` | Provides job market insights |
| `POST` | `/api/application-strategy` | Generates application strategies |
| `GET` | `/api/user/profile` | Retrieves user profile (auth required) |
| `POST` | `/api/auth/callback` | OAuth callback handler |

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.13+
- Node.js 18+
- Azure OpenAI access
- Azure Cosmos DB account
- Supabase account

### 1. Clone the Repository
```bash
git clone https://github.com/Praveenkumarbyrapuneni/genai-bootcamp.git
cd genai-bootcamp/projects/multi-agent-career-advisor
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start backend
cd api && uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with Supabase credentials

# Start frontend
npm run dev
```

### 4. Access the Application
Open [http://localhost:3000](http://localhost:3000) in your browser

---

## 🔐 Environment Variables

### Backend (`.env`)
```env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-10-21
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-ada-002

# Azure Cosmos DB
COSMOS_CONNECTION_STRING=your-cosmos-connection-string

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
```

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 💡 Skills Demonstrated

### 🤖 AI/ML Engineering
- Multi-agent AI system design and implementation
- Microsoft Semantic Kernel framework
- Prompt engineering and optimization
- RAG (Retrieval Augmented Generation) patterns
- Vector embeddings and semantic search

### ☁️ Cloud & Backend
- Azure OpenAI Service integration
- Azure Cosmos DB (NoSQL database)
- FastAPI REST API development
- OAuth 2.0 authentication flows
- Microservices architecture

### 🎨 Frontend Development
- Next.js 15 with App Router
- TypeScript
- Tailwind CSS
- Real-time UI updates
- Authentication state management

### 🛠 DevOps & Best Practices
- Environment configuration management
- Git version control
- Project documentation
- Code organization and modularity

---

## 📄 License

This project is part of the GenAI Bootcamp portfolio.

---

## 👨‍💻 Author

**Praveen Kumar Byrapuneni**

- GitHub: [@Praveenkumarbyrapuneni](https://github.com/Praveenkumarbyrapuneni)

---

<p align="center">
  Made with ❤️ using Microsoft Semantic Kernel and Azure OpenAI
</p>
