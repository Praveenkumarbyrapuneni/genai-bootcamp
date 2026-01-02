# 🚀 CareerPath AI - Multi-Agent Career Advisory System

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-16-black.svg)](https://nextjs.org)
[![Semantic Kernel](https://img.shields.io/badge/Semantic%20Kernel-1.39-purple.svg)](https://github.com/microsoft/semantic-kernel)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-green.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![Supabase](https://img.shields.io/badge/Supabase-Auth-orange.svg)](https://supabase.com)

An intelligent, AI-powered career advisory platform that uses **multiple specialized AI agents** to provide comprehensive career guidance, skill gap analysis, market research, and personalized job application strategies.

![CareerPath AI Banner](https://via.placeholder.com/1200x400/6366F1/FFFFFF?text=CareerPath+AI+-+Your+AI+Career+Strategist)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Multi-Agent System](#-multi-agent-system)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**CareerPath AI** is a sophisticated multi-agent system built using Microsoft's **Semantic Kernel** framework. It leverages the power of **Azure OpenAI GPT-4** to provide personalized career advice through a team of specialized AI agents, each with distinct expertise:

- 🎯 **Career Advisor** (Orchestrator) - Coordinates all agents and synthesizes recommendations
- 📊 **Market Researcher** - Analyzes job market trends and in-demand skills
- 🎓 **Skills Coach** - Assesses skill gaps and creates learning plans
- 📝 **Application Strategist** - Develops tailored job application strategies

---

## ✨ Features

### 🤖 AI-Powered Analysis
- **Comprehensive Career Analysis** - Full evaluation of your career trajectory
- **Skill Gap Assessment** - Identifies missing skills for your target role
- **Market Trend Analysis** - Real-time insights into job market demands
- **Personalized Learning Plans** - Custom roadmaps to acquire new skills
- **Application Strategy** - Tailored advice for job applications

### 🔐 Authentication & Security
- **GitHub OAuth** - Secure login with GitHub
- **Google OAuth** - Alternative authentication option
- **Supabase Authentication** - Enterprise-grade auth management
- **Session Management** - Persistent user sessions

### 💾 Data Persistence
- **Azure Cosmos DB** - Scalable NoSQL database for user data
- **Career Memory System** - Remembers your career history and preferences
- **Analysis History** - Track all past career analyses

### 🎨 Modern UI/UX
- **Next.js 16 Frontend** - Server-side rendered React application
- **Tailwind CSS** - Beautiful, responsive design
- **Rocket Launch Animation** - Engaging onboarding experience
- **Dark/Light Mode** - Customizable theme
- **Real-time Updates** - Live analysis progress

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Login     │  │  Dashboard  │  │   Analysis Results      │  │
│  │  (Supabase) │  │  Component  │  │      Component          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   /analyze  │  │  /history   │  │      /health            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 MULTI-AGENT SYSTEM (Semantic Kernel)             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  CAREER ADVISOR (Orchestrator)            │   │
│  │         Coordinates all agents & synthesizes advice       │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐     │
│  │   Market    │    │   Skills    │    │   Application   │     │
│  │ Researcher  │    │   Coach     │    │   Strategist    │     │
│  └─────────────┘    └─────────────┘    └─────────────────┘     │
│                                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌───────────┐  ┌───────────┐  ┌───────────┐
       │  Azure    │  │  Cosmos   │  │ Supabase  │
       │  OpenAI   │  │    DB     │  │   Auth    │
       └───────────┘  └───────────┘  └───────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.13 | Core programming language |
| **Semantic Kernel** | 1.39.0 | AI orchestration framework |
| **Azure OpenAI** | GPT-4 | Large Language Model |
| **FastAPI** | Latest | REST API framework |
| **Pydantic** | 2.11 | Data validation |
| **Azure Cosmos DB** | 4.5.1 | NoSQL database |
| **Supabase** | Latest | Authentication |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 16.1.1 | React framework |
| **React** | 19.2.3 | UI library |
| **TypeScript** | 5.x | Type safety |
| **Tailwind CSS** | 4.x | Styling |
| **Supabase Auth UI** | 0.4.7 | Auth components |

### Infrastructure
| Service | Purpose |
|---------|---------|
| **Azure OpenAI Service** | AI model hosting |
| **Azure Cosmos DB** | Data persistence |
| **Supabase** | Authentication & user management |
| **Vercel** (optional) | Frontend deployment |

---

## 🤖 Multi-Agent System

### Agent Details

#### 1. Career Advisor (Orchestrator)
```python
Role: "Career Strategy Orchestrator"
Expertise: ["Career strategy", "Team coordination", "Decision synthesis", "Comprehensive planning"]
```
**Responsibilities:**
- Coordinates all specialist agents
- Synthesizes multiple perspectives
- Provides final comprehensive recommendations
- Creates actionable career roadmaps

#### 2. Market Researcher
```python
Role: "Job Market Intelligence Specialist"
Expertise: ["Market analysis", "Trend identification", "Salary insights", "Industry research"]
```
**Responsibilities:**
- Analyzes current job market trends
- Identifies in-demand skills
- Provides salary benchmarks
- Tracks industry movements

#### 3. Skills Coach
```python
Role: "Professional Development Specialist"
Expertise: ["Skill assessment", "Learning paths", "Certification guidance", "Competency mapping"]
```
**Responsibilities:**
- Assesses current skill levels
- Identifies skill gaps
- Creates personalized learning plans
- Recommends certifications and courses

#### 4. Application Strategist
```python
Role: "Job Application Specialist"
Expertise: ["Resume optimization", "Interview prep", "Application timing", "Company targeting"]
```
**Responsibilities:**
- Develops application strategies
- Optimizes resume content
- Provides interview preparation
- Suggests target companies

---

## 📁 Project Structure

```
careerpath-ai/
├── 📁 api/
│   └── main.py                 # FastAPI backend server
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 app/
│   │   │   ├── layout.tsx      # Root layout
│   │   │   ├── page.tsx        # Home page
│   │   │   └── globals.css     # Global styles
│   │   ├── 📁 components/
│   │   │   ├── Dashboard.tsx   # Main dashboard
│   │   │   └── Login.tsx       # Login component
│   │   └── 📁 lib/
│   │       └── supabase.ts     # Supabase client
│   ├── package.json
│   ├── next.config.ts
│   └── tailwind.config.ts
├── 📁 src/
│   ├── kernel_config.py        # Semantic Kernel setup
│   ├── 📁 agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py       # Base agent class
│   │   ├── career_advisor.py   # Orchestrator agent
│   │   ├── market_researcher.py
│   │   ├── skills_coach.py
│   │   └── application_strategist.py
│   ├── 📁 auth/
│   │   ├── __init__.py
│   │   ├── auth_manager.py
│   │   ├── oauth_manager.py
│   │   └── supabase_auth.py    # Supabase OAuth
│   ├── 📁 database/
│   │   └── cosmos_manager.py   # Azure Cosmos DB
│   ├── 📁 memory/
│   │   └── career_memory.py    # Memory system
│   ├── 📁 planning/
│   │   └── career_planner.py   # Planning utilities
│   └── 📁 plugins/
│       └── 📁 job_intelligence/
│           ├── analyzer.py
│           └── scraper.py
├── 📁 prompts/
│   └── 📁 skills_analyzer/
│       └── extract_skills.txt  # Prompt templates
├── 📁 dashboard/
│   └── app.py                  # Streamlit dashboard
├── 📁 episodes/                # Tutorial episodes
│   ├── ep01_foundation/
│   ├── ep02_first_plugin/
│   ├── ep03_semantic_functions/
│   ├── ep04_memory_systems/
│   ├── ep05_planning/
│   ├── ep06_multi_agent/
│   └── ep07_persistence/
├── requirements.txt
├── startup.sh
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.13+
- Node.js 18+
- Azure OpenAI API access
- Supabase account
- Azure Cosmos DB account (optional)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/careerpath-ai.git
cd careerpath-ai
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Set Up Frontend
```bash
cd frontend
npm install
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
OAUTH_REDIRECT_URI=http://localhost:3000

# Azure Cosmos DB (Optional)
COSMOS_ENDPOINT=https://your-cosmos.documents.azure.com:443/
COSMOS_KEY=your-cosmos-key
COSMOS_DATABASE=careerpath
COSMOS_CONTAINER=analyses
```

---

## ⚙️ Configuration

### Azure OpenAI Setup
1. Create an Azure OpenAI resource in Azure Portal
2. Deploy a GPT-4 model
3. Copy the endpoint and API key to `.env`

### Supabase Setup
1. Create a new Supabase project
2. Enable GitHub OAuth in Authentication settings
3. Add redirect URL: `http://localhost:3000`
4. Copy project URL and anon key to `.env`

### Cosmos DB Setup (Optional)
1. Create an Azure Cosmos DB account
2. Create a database named `careerpath`
3. Create a container named `analyses`
4. Copy endpoint and key to `.env`

---

## 📖 Usage

### Start the Backend Server
```bash
# From root directory
cd api
uvicorn main:app --reload --port 8000
```

### Start the Frontend
```bash
# From frontend directory
cd frontend
npm run dev
```

### Access the Application
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Running Analysis
1. Log in with GitHub
2. Select your current skills
3. Enter your target role
4. Set your timeframe (1-12 months)
5. Click "Launch Career Analysis"
6. View comprehensive results from all agents

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check - API status |
| `GET` | `/health` | Detailed health check |
| `POST` | `/api/analyze` | Run career analysis |
| `GET` | `/api/history/{user_id}` | Get user's analysis history |

### Example API Request
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "target_role": "AI Engineer",
    "current_skills": ["Python", "Machine Learning", "SQL"],
    "timeframe_months": 6
  }'
```

### Example Response
```json
{
  "final_recommendations": "Based on your profile...",
  "market_research": "Current AI Engineer market trends...",
  "learning_plan": "Week 1-4: Focus on...",
  "application_strategy": "Target these companies first..."
}
```

---

## 📸 Screenshots

### Login Page
*Secure GitHub OAuth authentication*

### Dashboard
*Interactive skill selection and analysis configuration*

### Analysis Results
*Comprehensive career recommendations from all AI agents*

---

## 🔮 Future Enhancements

- [ ] **Resume Parser** - Automatically extract skills from uploaded resumes
- [ ] **Job Board Integration** - Real-time job listings from LinkedIn, Indeed
- [ ] **Interview Simulator** - AI-powered mock interviews
- [ ] **Progress Tracking** - Track skill development over time
- [ ] **Community Features** - Connect with others on similar career paths
- [ ] **Mobile App** - iOS/Android applications
- [ ] **Chrome Extension** - Analyze job postings directly from browser

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Praveen**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel) - AI orchestration framework
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) - GPT-4 model
- [Supabase](https://supabase.com) - Authentication
- [Next.js](https://nextjs.org) - React framework
- [Tailwind CSS](https://tailwindcss.com) - Styling

---

<p align="center">
  Made with ❤️ and 🤖 AI
</p>

<p align="center">
  <a href="#-careerpath-ai---multi-agent-career-advisory-system">Back to Top</a>
</p>
