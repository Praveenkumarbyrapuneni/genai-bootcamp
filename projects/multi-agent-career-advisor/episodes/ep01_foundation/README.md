# Episode 1: Foundation Setup

**Date Completed:** [Add today's date]  
**Duration:** ~30 minutes  
**Cost:** ~$0.0001

## 🎯 Goals Achieved

✅ Set up Python virtual environment  
✅ Installed Semantic Kernel  
✅ Configured Azure OpenAI connection  
✅ Created first AI interaction  
✅ Learned async/await basics

## 📁 Files Created

- `src/kernel_config.py` - Main kernel configuration
- `episodes/ep01_foundation/test_kernel.py` - First AI test
- `.env` - Environment variables (not in Git)
- `.gitignore` - Git ignore rules
- `requirements.txt` - Python dependencies

## 🧠 Key Concepts Learned

### 1. What is Semantic Kernel?
Semantic Kernel is an SDK that helps you build AI applications by:
- Managing connections to AI services (like Azure OpenAI)
- Orchestrating complex AI workflows
- Adding memory, plugins, and planning capabilities

### 2. The Kernel Object
The kernel is the central coordinator. Think of it as:
- A phone that connects to AI services
- A manager that coordinates different AI operations
- A container for AI capabilities

### 3. Async/Await
- `async def` - Declares a function that can wait without blocking
- `await` - Waits for an operation to complete
- Necessary because AI calls take time (network requests)

### 4. Environment Variables
- Store secrets safely in `.env`
- Never commit `.env` to Git
- Load with `python-dotenv`

## 🧪 What We Tested
```python
# I tested that our kernel can:
1. Connect to Azure OpenAI ✅
2. Send a prompt ✅
3. Receive a response ✅
```

## 💡 Next Steps (Episode 2)

In the next episode, we'll:
- Create our first **plugin**
- Learn the difference between **native** and **semantic** functions
- Build a job scraper that fetches real job data

## 🐛 Common Issues & Solutions

**Issue:** "Missing required environment variables"
- **Solution:** Check your `.env` file exists and has all values

**Issue:** "Module not found: semantic_kernel"
- **Solution:** Make sure venv is activated, run `pip install -r requirements.txt`

**Issue:** "Can't import kernel_config"
- **Solution:** Make sure you're running from the correct directory

## 📊 Cost Tracking

- API calls made: 1
- Tokens used: ~200
- Cost: ~$0.0001
- Remaining budget: $99.9999

