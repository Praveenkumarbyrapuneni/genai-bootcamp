# Episode 3: Semantic Functions & Skill Extraction

**Date Completed:** [Add today's date]  
**Duration:** ~60 minutes  
**Cost:** ~$0.03

## 🎯 Goals Achieved

✅ Created semantic functions (AI-powered)  
✅ Learned prompt engineering basics  
✅ Stored prompts in separate files  
✅ Extracted structured data from unstructured text  
✅ Compared skills with AI reasoning  
✅ Generated learning recommendations  
✅ Combined native + semantic functions  

## 📁 Files Created

- `prompts/skills_analyzer/extract_skills.txt` - Skill extraction prompt
- `src/plugins/job_intelligence/analyzer.py` - Semantic functions plugin
- `episodes/ep03_semantic_functions/test_skills_analyzer.py` - Tests
- `episodes/ep03_semantic_functions/README.md` - This file

## 🧠 Key Concepts Learned

### 1. Semantic Functions

**Definition:** Functions that use LLM (AI) to process text and reason about content.

**How they work:**
```
Prompt Template → Replace Variables → Send to AI → Parse Response
```

**Characteristics:**
- Non-deterministic (varies slightly)
- Costs tokens (money)
- Can understand context and nuance
- Great for: analysis, extraction, reasoning

### 2. Prompt Engineering

**What is it?** The art of writing prompts that get good AI responses.

**Best practices we used:**
- Clear instructions
- Specify output format (JSON)
- Give examples
- Be explicit about what you want
- Tell AI to return ONLY the format you need

**Example:**
```
Bad prompt: "Extract skills"
Good prompt: "Extract all technical skills. Return as JSON: {skills: [...]}"
```

### 3. Variable Substitution

**In prompt templates:**
```
{{$input}} - Gets replaced with your actual input
{{$variable_name}} - Any variable you pass
```

**In code:**
```python
await kernel.invoke_prompt(
    prompt=template,
    arguments={"input": "actual value"}
)
```

### 4. Structured Output

**Challenge:** AI returns text, we need structured data

**Solution:**
1. Ask for JSON in prompt
2. Clean markdown formatting
3. Parse JSON
4. Handle errors gracefully

### 5. Combining Functions

**Power of Semantic Kernel:**
- Native function scrapes data (fast, free)
- Semantic function analyzes it (smart, costs tokens)
- Together = powerful pipeline!

## 🆚 Native vs Semantic Functions - Complete Comparison

| Aspect | Native Function | Semantic Function |
|--------|----------------|-------------------|
| **Written in** | Python code | Text prompts |
| **Uses AI?** | No | Yes |
| **Cost** | Free | ~$0.001-0.01 per call |
| **Speed** | Very fast (<1ms) | Slower (1-3 seconds) |
| **Deterministic?** | Yes (same input = same output) | No (varies slightly) |
| **Good for** | Data fetching, math, APIs | Understanding, reasoning, analysis |
| **Needs kernel?** | No | Yes (to access AI service) |
| **Example** | Scrape jobs from API | Extract skills from text |

## 🧪 What We Tested

1. ✅ Extract skills from job description
2. ✅ Compare candidate skills to job (AI reasoning)
3. ✅ Generate personalized learning plan
4. ✅ Full pipeline: scrape + analyze

## 💡 Prompt Engineering Tips

### Tip 1: Be Specific
```
❌ "Analyze this job"
✅ "Extract technical skills, experience level, and education requirements"
```

### Tip 2: Specify Format
```
❌ "List the skills"
✅ "Return ONLY valid JSON: {skills: [...]}"
```

### Tip 3: Give Context
```
❌ "Extract skills"
✅ "You are an expert recruiter. Extract ALL technical skills mentioned..."
```

### Tip 4: Handle Edge Cases
```
"If no skills are found, return empty array []"
"If experience is not mentioned, return 'not specified'"
```

### Tip 5: Clean Output
```python
# AI sometimes adds markdown
if result.startswith("```json"):
    result = result[7:-3]  # Remove ```json and ```
```

## 📊 Token Usage

**Typical token counts:**
- Short job description: 500-1000 tokens
- Skill extraction response: 200-400 tokens
- Comparison analysis: 600-1000 tokens
- Learning plan: 1000-2000 tokens

**Cost with GPT-4o-mini:**
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens
- Average call: $0.0005-0.002

## 🔄 Workflow Example
```python
# 1. Scrape jobs (Native - Free)
jobs = await scraper.scrape_genai_jobs(keywords="AI")

# 2. Analyze with AI (Semantic - ~$0.001)
skills = await analyzer.extract_skills_from_job(jobs[0])

# 3. Compare to profile (Semantic - ~$0.001)
match = await analyzer.compare_skills_to_profile(skills, my_skills)

# 4. Generate plan (Semantic - ~$0.002)
plan = await analyzer.generate_learning_recommendations(gaps)

Total cost: ~$0.004 (less than half a cent!)
```

## 💡 Next Steps (Episode 4)

In the next episode, we'll add **memory** to our system:
- Store your skills and progress
- Remember past analyses
- Build a knowledge base
- Use embeddings for semantic search

## 🐛 Common Issues & Solutions

**Issue:** "AI returns invalid JSON"
- **Solution:** Improve prompt, add "ONLY valid JSON, no markdown"

**Issue:** "Prompt template not found"
- **Solution:** Check file path: `prompts/skills_analyzer/extract_skills.txt`

**Issue:** "Response varies too much"
- **Solution:** Add temperature parameter (lower = more consistent)

**Issue:** "AI ignores instructions"
- **Solution:** Be more explicit, use stronger language

## 📊 Cost Tracking

- Episode 1: $0.0001
- Episode 2: $0.00
- Episode 3: $0.03
- **Total Spent:** $0.0301
- **Remaining:** $99.97
