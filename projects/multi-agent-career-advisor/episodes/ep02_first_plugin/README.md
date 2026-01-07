# Episode 2: First Plugin - Job Scraper

**Date Completed:** [Add today's date]  
**Duration:** ~45 minutes  
**Cost:** $0 (free APIs only)

## 🎯 Goals Achieved

✅ Understood native vs semantic functions  
✅ Created first plugin class  
✅ Used `@kernel_function` decorator  
✅ Integrated external APIs (Remotive, Arbeitnow)  
✅ Implemented error handling  
✅ Added plugin to kernel  
✅ Tested plugin functions

## 📁 Files Created

- `src/plugins/job_intelligence/scraper.py` - Main plugin
- `src/plugins/job_intelligence/__init__.py` - Package init
- `src/plugins/__init__.py` - Plugins package init
- `episodes/ep02_first_plugin/test_job_scraper.py` - Tests

## 🧠 Key Concepts Learned

### 1. Native Functions
**Definition:** Functions written in Python code that perform specific tasks.

**Characteristics:**
- Deterministic (predictable output)
- Fast execution
- No AI/LLM required
- Good for: data fetching, calculations, API calls

**Example:**
```python
@kernel_function(name="scrape_jobs", description="...")
async def scrape_genai_jobs(self, keywords: str) -> str:
    # Fetch from API
    return json.dumps(results)
```

### 2. Plugin Architecture

**What's a Plugin?**
- A collection of related functions
- Organized as a Python class
- Can be added to the kernel
- Makes functions available to AI planners

**Structure:**
```python
class JobScraperPlugin:
    @kernel_function(...)
    async def function_one(self):
        pass
    
    @kernel_function(...)
    async def function_two(self):
        pass
```

### 3. The @kernel_function Decorator

**Purpose:** Registers a method as a kernel function

**Required attributes:**
- `name` - Function identifier
- `description` - Explains what it does (for AI planners!)

**Why important?**
Later, when we build AI planners, they'll read these descriptions
to decide which functions to use!

### 4. Async HTTP Requests

**Why async?**
- Can fetch from multiple sources simultaneously
- Doesn't block while waiting for responses
- More efficient for I/O operations

**Pattern:**
```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()
```

### 5. Adding Plugins to Kernel
```python
kernel.add_plugin(
    plugin=my_plugin_instance,
    plugin_name="plugin_name"
)
```

This makes all `@kernel_function` methods available through the kernel.

## 🔄 Native vs Semantic Functions

| Aspect | Native Function | Semantic Function |
|--------|----------------|-------------------|
| **Written in** | Python code | AI prompts |
| **Uses LLM?** | No | Yes |
| **Cost** | Free | Costs tokens |
| **Deterministic?** | Yes | No (varies) |
| **Speed** | Fast | Slower (API call) |
| **Best for** | Data fetching, calculations | Text analysis, reasoning |

**In this episode:** We built native functions  
**Next episode:** We'll build semantic functions!

## 🧪 What We Tested

1. ✅ Direct plugin function calls
2. ✅ Plugin registration with kernel
3. ✅ Invoking functions through kernel
4. ✅ Multiple functions in one plugin
5. ✅ Error handling with failed API calls
6. ✅ Real data from external APIs

## 📊 APIs Used

### Remotive API
- **URL:** https://remotive.com/api/remote-jobs
- **Cost:** Free, no authentication
- **Rate limit:** None documented
- **Data:** Remote jobs worldwide

### Arbeitnow API
- **URL:** https://www.arbeitnow.com/api/job-board-api
- **Cost:** Free, no authentication
- **Rate limit:** Unspecified
- **Data:** European jobs primarily

## 💡 Next Steps (Episode 3)

In the next episode, we'll:
- Create **semantic functions** (AI-powered!)
- Build a skill extraction system
- Learn prompt engineering
- Use AI to analyze job descriptions

## 🐛 Common Issues & Solutions

**Issue:** "aiohttp module not found"
- **Solution:** `pip install aiohttp==3.9.1`

**Issue:** "No jobs found"
- **Solution:** APIs might be slow/down. Try different keywords.

**Issue:** "Plugin not found in kernel"
- **Solution:** Make sure you called `kernel.add_plugin()` first

**Issue:** "JSON decode error"
- **Solution:** API returned invalid JSON. Check error handling.

## 📊 Cost Tracking

- API calls made: ~6 (2 APIs × 3 tests)
- AI calls made: 0
- Cost: $0.00
- Remaining budget: $100.00
