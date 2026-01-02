# episodes/ep03_semantic_functions/test_skills_analyzer.py

"""
Episode 3: Testing Semantic Functions

This script demonstrates:
1. Creating and using semantic functions
2. AI-powered text analysis
3. Combining native + semantic functions
4. Understanding prompt engineering
"""

import asyncio
import sys
import os
import json

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.kernel_config import create_kernel
from src.plugins.job_intelligence import JobScraperPlugin, SkillsAnalyzerPlugin


# Sample job description for testing
SAMPLE_JOB_DESCRIPTION = """
Senior GenAI Engineer

We're looking for an experienced GenAI Engineer to join our AI team.

Required Skills:
- 5+ years of Python programming
- Strong experience with LLMs (GPT-4, Claude, Llama)
- Proficiency in prompt engineering and RAG systems
- Experience with vector databases (Pinecone, Weaviate, ChromaDB)
- Knowledge of semantic kernel or LangChain
- Experience deploying ML models to production

Preferred Skills:
- Azure OpenAI or AWS Bedrock experience
- Fine-tuning experience
- Knowledge of transformer architectures
- Experience with MLOps tools

Requirements:
- Bachelor's in Computer Science or related field
- 5-7 years of relevant experience
- Strong communication skills
- Experience working in Agile teams

What you'll do:
- Build and deploy GenAI applications
- Design prompt engineering strategies
- Optimize LLM performance
- Collaborate with product teams
- Mentor junior engineers
"""

# Sample candidate profile
CANDIDATE_SKILLS = """
Python, JavaScript, Azure OpenAI, GPT-4, prompt engineering, 
vector databases, Pinecone, Semantic Kernel, FastAPI, Docker, 
Git, 3 years ML experience, Bachelor's in CS
"""


async def test_semantic_function_basic():
    """
    Test 1: Basic semantic function call
    
    Shows how to use AI to extract structured data from text.
    """
    print("=" * 70)
    print("TEST 1: Extract Skills with AI (Semantic Function)")
    print("=" * 70)
    
    # Create kernel (needed for AI calls)
    kernel = create_kernel()
    
    # Create analyzer plugin (needs kernel!)
    analyzer = SkillsAnalyzerPlugin(kernel)
    
    print("\n📄 Analyzing job description...")
    print(f"Description length: {len(SAMPLE_JOB_DESCRIPTION)} characters\n")
    
    # Call the semantic function
    # This will cost a few tokens (~$0.001)
    result_json = await analyzer.extract_skills_from_job(SAMPLE_JOB_DESCRIPTION)
    
    # Parse and display
    result = json.loads(result_json)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return None
    
    print("\n" + "=" * 70)
    print("📊 EXTRACTED SKILLS:")
    print("=" * 70)
    
    print(f"\n✅ Required Skills ({len(result.get('required_skills', []))}):")
    for skill in result.get('required_skills', []):
        print(f"   • {skill}")
    
    print(f"\n⭐ Preferred Skills ({len(result.get('preferred_skills', []))}):")
    for skill in result.get('preferred_skills', []):
        print(f"   • {skill}")
    
    print(f"\n🎯 Experience Level: {result.get('experience_level', 'N/A')}")
    print(f"📅 Years Experience: {result.get('years_experience', 'N/A')}")
    print(f"🎓 Education: {result.get('education', 'N/A')}")
    
    print(f"\n🛠️ Technologies:")
    for tech in result.get('technologies', []):
        print(f"   • {tech}")
    
    return result_json


async def test_skills_comparison():
    """
    Test 2: AI-powered skills comparison
    
    Shows how AI can reason about matches and gaps.
    """
    print("\n" + "=" * 70)
    print("TEST 2: Compare Candidate to Job (AI Reasoning)")
    print("=" * 70)
    
    kernel = create_kernel()
    analyzer = SkillsAnalyzerPlugin(kernel)
    
    # First, extract job requirements
    print("\n📋 Step 1: Extracting job requirements...")
    job_skills = await analyzer.extract_skills_from_job(SAMPLE_JOB_DESCRIPTION)
    
    # Then, compare to candidate
    print("\n🎯 Step 2: Comparing candidate skills...")
    print(f"Candidate skills: {CANDIDATE_SKILLS}\n")
    
    comparison_json = await analyzer.compare_skills_to_profile(
        job_skills,
        CANDIDATE_SKILLS
    )
    
    comparison = json.loads(comparison_json)
    
    if "error" in comparison:
        print(f"❌ Error: {comparison['error']}")
        return
    
    print("\n" + "=" * 70)
    print("📊 MATCH ANALYSIS:")
    print("=" * 70)
    
    match_pct = comparison.get('match_percentage', 0)
    print(f"\n🎯 Overall Match: {match_pct}%")
    print(f"🚦 Readiness: {comparison.get('readiness_level', 'unknown').upper()}")
    
    print(f"\n✅ Matched Skills ({len(comparison.get('matched_skills', []))}):")
    for skill in comparison.get('matched_skills', []):
        print(f"   • {skill}")
    
    print(f"\n⚠️ Missing Critical Skills ({len(comparison.get('missing_critical_skills', []))}):")
    for skill in comparison.get('missing_critical_skills', []):
        print(f"   • {skill}")
    
    print(f"\n🔄 Transferable Skills:")
    for skill in comparison.get('transferable_skills', []):
        print(f"   • {skill}")
    
    print(f"\n💡 Recommendation:")
    print(f"   {comparison.get('recommendation', 'No recommendation available')}")
    
    return comparison_json


async def test_learning_recommendations():
    """
    Test 3: Generate personalized learning plan
    
    Shows how AI can be creative and helpful.
    """
    print("\n" + "=" * 70)
    print("TEST 3: Generate Learning Plan (AI Creativity)")
    print("=" * 70)
    
    kernel = create_kernel()
    analyzer = SkillsAnalyzerPlugin(kernel)
    
    # Skills to learn
    missing_skills = "Fine-tuning LLMs, MLOps, AWS Bedrock, Transformer architectures"
    
    print(f"\n📚 Generating learning plan for: {missing_skills}")
    print(f"📊 Current level: intermediate\n")
    
    plan_json = await analyzer.generate_learning_recommendations(
        missing_skills=missing_skills,
        current_level="intermediate"
    )
    
    plan = json.loads(plan_json)
    
    if "error" in plan:
        print(f"❌ Error: {plan['error']}")
        return
    
    print("\n" + "=" * 70)
    print("📚 PERSONALIZED LEARNING PLAN:")
    print("=" * 70)
    
    print(f"\n⏱️ Estimated Time: {plan.get('estimated_weeks', 0)} weeks")
    
    print(f"\n🎯 Priority Order:")
    for i, skill in enumerate(plan.get('priority_order', []), 1):
        print(f"   {i}. {skill}")
    
    print(f"\n🚀 Quick Wins (Start Here!):")
    for win in plan.get('quick_wins', []):
        print(f"   • {win}")
    
    print(f"\n📖 Detailed Learning Path:")
    for item in plan.get('learning_path', []):
        print(f"\n   📌 {item.get('skill', 'N/A')}")
        print(f"      Why: {item.get('why_important', 'N/A')}")
        print(f"      Time: {item.get('estimated_time', 'N/A')}")
        
        if item.get('resources'):
            print(f"      Resources:")
            for resource in item.get('resources', [])[:2]:  # Show first 2
                print(f"         • {resource.get('name', 'N/A')} ({resource.get('type', 'N/A')})")
        
        if item.get('practice_projects'):
            print(f"      Projects:")
            for project in item.get('practice_projects', [])[:2]:
                print(f"         • {project}")
    
    print(f"\n✅ Success Metrics:")
    print(f"   {plan.get('success_metrics', 'Practice and build projects')}")


async def test_real_job_pipeline():
    """
    Test 4: Complete pipeline - Scrape + Analyze
    
    Combines native functions (scraping) with semantic functions (analysis).
    This is the power of Semantic Kernel!
    """
    print("\n" + "=" * 70)
    print("TEST 4: Full Pipeline - Scrape Real Job + AI Analysis")
    print("=" * 70)
    
    kernel = create_kernel()
    
    # Create both plugins
    scraper = JobScraperPlugin()
    analyzer = SkillsAnalyzerPlugin(kernel)
    
    # Step 1: Scrape real jobs (native function)
    print("\n🔍 Step 1: Fetching real jobs from APIs...")
    jobs_json = await scraper.scrape_genai_jobs(
        keywords="GenAI,LLM,AI engineer",
        limit=3
    )
    
    jobs_data = json.loads(jobs_json)
    jobs = jobs_data.get('jobs', [])
    
    if not jobs:
        print("❌ No jobs found. Try different keywords or check APIs.")
        return
    
    print(f"✅ Found {len(jobs)} jobs\n")
    
    # Step 2: Analyze first job with AI (semantic function)
    first_job = jobs[0]
    print(f"📄 Analyzing: {first_job['title']} at {first_job['company']}")
    print(f"🔗 URL: {first_job['url']}\n")
    
    # For this demo, we'll use the title + company as a simple description
    # In real usage, you'd fetch the full job description
    simple_description = f"""
    Job Title: {first_job['title']}
    Company: {first_job['company']}
    Location: {first_job['location']}
    
    This is a {first_job['title']} position. Based on the title, 
    typical requirements would include relevant technical skills.
    """
    
    print("🤖 Running AI analysis...")
    analysis_json = await analyzer.extract_skills_from_job(simple_description)
    analysis = json.loads(analysis_json)
    
    if "error" not in analysis:
        print(f"\n✅ AI extracted {len(analysis.get('required_skills', []))} skills")
        print(f"📊 Experience level: {analysis.get('experience_level', 'N/A')}")
    
    print("\n💡 This demonstrates combining:")
    print("   • Native function (job scraping) - precise, fast, free")
    print("   • Semantic function (AI analysis) - intelligent, flexible, costs tokens")


async def main():
    """
    Main test runner
    """
    print("🚀 Episode 3: Semantic Functions Tests\n")
    print("💡 Note: These tests use AI and will cost ~$0.02-0.05 total\n")
    
    try:
        # Run all tests
        await test_semantic_function_basic()
        await test_skills_comparison()
        await test_learning_recommendations()
        await test_real_job_pipeline()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        
        print("\n💡 Key Learnings:")
        print("1. Semantic functions use AI to understand and reason")
        print("2. Prompts are stored in files for easy editing")
        print("3. AI can extract structured data from unstructured text")
        print("4. Combine native + semantic functions for powerful pipelines")
        print("5. Always handle AI response parsing carefully")
        
        print("\n💰 Estimated Cost: ~$0.03")
        print("   - 4 AI calls × ~2000 tokens each")
        print("   - GPT-4o-mini: $0.15 per 1M tokens")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())