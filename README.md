# 🚀 CareerPath AI - Brutally Honest Career Advisor

> **AI-powered career advisor that gives REAL advice, not motivational speeches.**

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://icy-grass-0516c410f.6.azurestaticapps.net)
[![Backend](https://img.shields.io/badge/Backend-Azure-blue)](https://careerpath-api.thankfulsea-42148813.eastus.azurecontainerapps.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 **What This App Does**

CareerPath AI is a **brutally honest career advisor** that:
- ✅ Analyzes your resume deeply (experience, projects, education)
- ✅ Gives you a **reality check** on your career readiness
- ✅ Provides personalized learning plans
- ✅ Tells you which companies you're ready for
- ✅ Estimates your actual callback rate

**No sugar-coating. Just honest, actionable advice.**

---

## 🏗️ **Tech Stack**

### **Frontend**
- **Framework:** Next.js 15 (React, TypeScript)
- **Styling:** Tailwind CSS
- **Auth:** Supabase (GitHub & Google OAuth)
- **Hosting:** Azure Static Web Apps

### **Backend**
- **Framework:** FastAPI (Python)
- **AI Engine:** Groq (FREE & 10x faster than Azure OpenAI!)
- **Model:** Llama 3.3 70B Versatile
- **Hosting:** Azure Container Apps
- **Database:** Azure Cosmos DB (NoSQL)
- **Tracking:** Supabase PostgreSQL

### **AI Architecture**
- **Multi-Agent System:**
  - Career Advisor (Orchestrator)
  - Market Researcher
  - Skills Coach
  - Application Strategist
- **Resume Parser:** PyPDF2, python-docx
- **Response Time:** 2-5 seconds ⚡

---

## 🔐 **Security & API Keys**

All sensitive credentials are stored securely:

### **Where API Keys Are Located:**

| Service | Local (.env) | Azure Container Apps | Azure Static Web Apps |
|---------|--------------|----------------------|-----------------------|
| **Groq API** | ✅ `.env` | ✅ Environment Variables | ❌ Not needed |
| **Cosmos DB** | ✅ `.env` | ✅ Environment Variables | ❌ Not needed |
| **Supabase** | ✅ `frontend/.env.local` | ✅ Environment Variables | ✅ Configuration |

### **API Keys Used:**

1. **Groq API Key** (FREE)
   - Location: `.env` file (backend)
   - Used for: Fast LLM responses (2-3 seconds!)
   - Get yours: https://console.groq.com

2. **Azure Cosmos DB**
   - Location: `.env` file (backend)
   - Used for: Storing career analysis history

3. **Supabase**
   - Location: `frontend/.env.local` & `.env`
   - Used for: Authentication & search tracking

### **🔒 Security Best Practices:**

✅ **Never commit `.env` files to GitHub** (already in `.gitignore`)
✅ All API keys stored as Azure environment variables in production
✅ Supabase Row Level Security (RLS) enabled
✅ CORS properly configured
✅ No API keys exposed in frontend code

---

## 📂 **Project Structure**

```
careerpath-with-auth/
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js 15 App Router
│   │   ├── components/    # React components
│   │   │   ├── Dashboard.tsx      # Main career advisor UI
│   │   │   ├── Login.tsx          # Auth page
│   │   │   └── HistoryManager.tsx # Analysis history
│   │   └── lib/
│   │       └── supabase.ts        # Supabase client
│   └── .env.local         # Frontend environment variables
│
├── api/                   # FastAPI backend
│   └── main.py           # API endpoints
│
├── src/                  # AI agents & logic
│   ├── groq_client.py    # Groq LLM client (FAST!)
│   ├── kernel_config.py  # AI kernel setup
│   ├── agents/           # Multi-agent system
│   │   ├── career_advisor.py        # Main orchestrator
│   │   ├── market_researcher.py     # Job market analysis
│   │   ├── skills_coach.py          # Learning plans
│   │   └── application_strategist.py # Application advice
│   └── database/
│       ├── cosmos_manager.py   # Cosmos DB integration
│       └── supabase_tracker.py # Search analytics
│
├── .env                  # Backend environment variables
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container image config
└── README.md           # This file
```

---

## 🚀 **Quick Start**

### **Prerequisites**
- Node.js 18+
- Python 3.11+
- Docker (for deployment)
- Azure CLI (for deployment)

### **1. Clone the Repository**

```bash
git clone <your-github-repo-url>
cd careerpath-with-auth
```

### **2. Set Up Backend**

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
# Groq Configuration (FREE & FAST)
GROQ_API_KEY=your_groq_api_key_here
USE_GROQ=true

# Azure Cosmos DB
COSMOS_CONNECTION_STRING=your_cosmos_connection_string

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
EOF

# Run backend locally
python -m uvicorn api.main:app --reload
# Backend runs at: http://localhost:8000
```

### **3. Set Up Frontend**

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << 'EOF'
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

# Run frontend locally
npm run dev
# Frontend runs at: http://localhost:3000
```

### **4. Visit the App**

Open http://localhost:3000 and sign in with GitHub or Google!

---

## ☁️ **Deployment to Azure**

### **Backend Deployment (Azure Container Apps)**

```bash
# Build Docker image
docker build -t careerpathacr73131.azurecr.io/careerpath-api:latest .

# Push to Azure Container Registry
docker push careerpathacr73131.azurecr.io/careerpath-api:latest

# Deploy to Azure Container Apps
az containerapp update \
  --name careerpath-api \
  --resource-group careerpath-rg \
  --image careerpathacr73131.azurecr.io/careerpath-api:latest \
  --set-env-vars \
    GROQ_API_KEY="your_key" \
    USE_GROQ="true" \
    COSMOS_CONNECTION_STRING="your_cosmos_connection" \
    SUPABASE_URL="your_supabase_url" \
    SUPABASE_ANON_KEY="your_supabase_key"
```

**Backend URL:** https://careerpath-api.thankfulsea-42148813.eastus.azurecontainerapps.io

### **Frontend Deployment (Azure Static Web Apps)**

```bash
cd frontend

# Build for production
npm run build

# Deploy to Azure Static Web Apps
npx @azure/static-web-apps-cli deploy out \
  --deployment-token $(az staticwebapp secrets list \
    --name careerpath-frontend \
    --query "properties.apiKey" -o tsv) \
  --env production
```

**Frontend URL:** https://icy-grass-0516c410f.6.azurestaticapps.net

---

## 🎯 **Key Features**

### **1. Resume Analysis**
- Deep analysis of work experience, projects, education
- Extracts skills automatically
- Calculates real readiness score (0-100%)
- Compares to market requirements

### **2. Multi-Tab Results**
- **Reality Check:** Brutally honest assessment
- **Market Fit:** Job market analysis
- **Learning Plan:** Personalized roadmap
- **Application Strategy:** When and where to apply

### **3. Skills Management**
- 30+ pre-defined skills
- Add custom skills
- Auto-extraction from resume
- Skill gap analysis

### **4. Chat History**
- Save past analyses
- Quick access to previous sessions
- Delete/manage conversations

### **5. Fast AI Responses**
- **Groq LLM:** 2-5 second responses
- **Previous (Azure OpenAI):** 15+ minutes 🐌
- **10x speed improvement!** ⚡

---

## 🔧 **Environment Variables Reference**

### **Backend (.env)**
```bash
# Groq API (FREE)
GROQ_API_KEY=<GROQ_API_KEY_REMOVED>
USE_GROQ=true

# Azure Cosmos DB
COSMOS_CONNECTION_STRING=AccountEndpoint=https://...

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
```

### **Frontend (frontend/.env.local)**
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000  # Local
# NEXT_PUBLIC_API_URL=https://careerpath-api.thankfulsea-42148813.eastus.azurecontainerapps.io  # Production
```

---

## 📊 **API Endpoints**

### **Backend API**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/analyze` | POST | Run career analysis |
| `/api/parse-resume` | POST | Parse uploaded resume |
| `/api/history/{user_id}` | GET | Get user's analysis history |
| `/api/history/bulk-delete` | POST | Delete multiple analyses |
| `/api/analytics/searches` | GET | Get all searches (admin) |
| `/api/analytics/popular-roles` | GET | Most searched roles |
| `/api/user/{user_id}/searches` | GET | User's search history |

### **Example Request**

```bash
curl -X POST https://careerpath-api.thankfulsea-42148813.eastus.azurecontainerapps.io/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "target_role": "Data Analyst",
    "current_skills": ["Python", "SQL", "Excel"],
    "timeframe_months": 6,
    "timeframe_display": "6 months"
  }'
```

---

## 🧪 **Testing**

### **Test Backend Locally**
```bash
# Test if backend is running
curl http://localhost:8000/

# Test analysis endpoint
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","target_role":"hello","current_skills":[],"timeframe_months":6}'
```

### **Test Groq Integration**
```bash
python3 -c "
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
response = client.chat.completions.create(
    model='llama-3.3-70b-versatile',
    messages=[{'role': 'user', 'content': 'Say hello!'}],
    max_tokens=50
)
print(response.choices[0].message.content)
"
```

---

## 📈 **Performance Metrics**

| Metric | Azure OpenAI | Groq | Improvement |
|--------|--------------|------|-------------|
| **First Response** | 15+ min 🐌 | 2-5 sec ⚡ | **180x faster** |
| **Subsequent Requests** | 10-30 sec | 2-5 sec | **5x faster** |
| **Cost** | $0.15/1M tokens | FREE | **100% savings** |
| **Rate Limit** | Low | 14,400/day | **Much higher** |

---

## 🐛 **Troubleshooting**

### **Backend not starting?**
- Check `.env` file exists with all required keys
- Verify Groq API key is valid
- Run: `python3 -c "from src.kernel_config import create_kernel"`

### **Frontend shows "Unable to analyze"?**
- Check backend is running (`http://localhost:8000`)
- Verify `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Check browser console for errors

### **Slow responses on Azure?**
- Azure Container Apps has 2-3 min cold start
- First request after idle is slow
- Subsequent requests are fast (2-5 sec)

### **Groq API errors?**
- Check API key is correct in `.env`
- Verify `USE_GROQ=true` is set
- Check Groq rate limits (14,400 requests/day)

---

## 🎓 **How It Works**

### **AI Agent Architecture**

```
User Request → Career Advisor (Orchestrator)
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
 Market Researcher  Skills Coach  Application Strategist
        ↓             ↓             ↓
        └─────────────┼─────────────┘
                      ↓
              Synthesized Response
```

### **Request Flow**

1. **User inputs:** Target role, skills, resume (optional)
2. **Frontend:** Sends request to FastAPI backend
3. **Backend:** 
   - Validates input
   - Extracts resume data (if provided)
   - Routes to Career Advisor agent
4. **Career Advisor:**
   - Analyzes resume deeply
   - Delegates to specialist agents
   - Synthesizes responses
5. **Groq LLM:** Generates honest, personalized advice (2-5 sec)
6. **Database:** Saves analysis to Cosmos DB
7. **Frontend:** Displays results in 4 tabs

---

## 📝 **To-Do / Future Improvements**

- [ ] Add interview prep questions
- [ ] Company-specific advice (FAANG, startups, etc.)
- [ ] Salary negotiation tips
- [ ] LinkedIn profile optimization
- [ ] Mock interview simulator
- [ ] Job application tracker
- [ ] Networking strategies

---

## 🤝 **Contributing**

Pull requests welcome! For major changes, please open an issue first.

---

## 📄 **License**

MIT License - feel free to use this for your own projects!

---

## 👨‍💻 **Author**

**Praveen**
- GitHub: [Your GitHub Profile]
- LinkedIn: [Your LinkedIn]
- Demo: https://icy-grass-0516c410f.6.azurestaticapps.net

---

## 🙏 **Acknowledgments**

- **Groq** for blazing-fast FREE LLM API
- **Azure** for cloud hosting
- **Supabase** for authentication
- **Microsoft Semantic Kernel** for AI orchestration
- **Next.js** for amazing developer experience

---

## 📞 **Support**

Having issues? [Open an issue](https://github.com/your-repo/issues) or contact me!

---

**Built with ❤️ and brutal honesty** 💪
