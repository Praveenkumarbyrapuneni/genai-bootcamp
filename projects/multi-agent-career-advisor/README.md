# 🚀 CareerPath AI

**An AI-powered career strategist for GenAI engineers**

Built with Microsoft Semantic Kernel | Deployed on Azure | Budget: $5/month

## 📖 About This Project

CareerPath AI is a multi-agent system that helps aspiring GenAI engineers strategically position themselves in the job market. Unlike simple job application bots, this agent:

- 📊 Analyzes real-time job market trends
- 🎯 Identifies your skills gaps
- 📚 Creates personalized learning plans
- 🤖 Uses multi-agent coordination
- 💰 Runs on just $5/month

Documenting the complete process of building a production AI agent from scratch.

## 🎥 Video Series

This project is being built as a 10-episode video series:

- [x] **Episode 1:** Foundation Setup ✅
- [ ] **Episode 2:** First Plugin (Job Scraper)
- [ ] **Episode 3:** Semantic Functions & Skill Extraction
- [ ] **Episode 4:** Memory Systems
- [ ] **Episode 5:** Planning & Orchestration
- [ ] **Episode 6:** External Tools Integration
- [ ] **Episode 7:** Multi-Agent Architecture
- [ ] **Episode 8:** Persistent Storage (Cosmos DB)
- [ ] **Episode 9:** Azure Functions Deployment
- [ ] **Episode 10:** Dashboard & Demo

## 🛠️ Tech Stack

- **AI Framework:** Semantic Kernel (Python)
- **LLM:** Azure OpenAI GPT-4o-mini
- **Memory:** Azure Cosmos DB (free tier)
- **Deployment:** Azure Functions (consumption plan)
- **Dashboard:** Streamlit
- **Version Control:** Git/GitHub

## 📁 Project Structure
```
careerpathai/
├── src/                    # Main source code
│   ├── kernel_config.py   # Kernel setup
│   ├── plugins/           # AI plugins
│   ├── agents/            # Multi-agent system
│   └── memory/            # Memory management
├── episodes/              # Episode-specific code
│   ├── ep01_foundation/
│   ├── ep02_first_plugin/
│   └── ...
├── prompts/               # Prompt templates
├── tests/                 # Unit tests
├── docs/                  # Documentation
└── requirements.txt       # Dependencies
```

## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/careerpathai.git
cd careerpathai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and add your keys
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# Test the setup
python episodes/ep01_foundation/test_kernel.py
```

## 🔑 Required Credentials

You'll need:
- Azure OpenAI API key and endpoint
- Azure Cosmos DB connection string (for Episode 8+)

## 💰 Cost Breakdown

| Service | Monthly Cost | Notes |
|---------|-------------|--------|
| Azure OpenAI (GPT-4o-mini) | $3-5 | ~20k tokens/day |
| Text Embeddings | $1-2 | Memory operations |
| Azure Functions | $0 | Free tier |
| Cosmos DB | $0 | Free tier |
| **Total** | **$4-7** | Well within budget! |

## 📚 Learning Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [Episode-specific READMEs](./episodes/)

## 🤝 Contributing

This is primarily a learning project, but suggestions and feedback are welcome!

## 📄 License

MIT License 

##  Author

Built by PRAVEEN KUMAR BYRAPUNENI as a learning journey into GenAI engineering

##  Acknowledgments

- Microsoft for Semantic Kernel
- Azure for student credits
- The GenAI community for inspiration

---
