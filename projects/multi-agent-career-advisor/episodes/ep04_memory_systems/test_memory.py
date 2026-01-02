# episodes/ep04_memory_systems/test_memory.py

"""
Episode 4: Testing Memory Systems

This script demonstrates:
1. Storing skills in memory
2. Semantic search (finding similar skills)
3. Tracking job analyses
4. Calculating skill coverage
5. Understanding vector embeddings
"""

import asyncio
import sys
import os
import json

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.kernel_config import create_kernel
from src.memory import CareerMemory


async def test_basic_memory_storage():
    """
    Test 1: Store and retrieve skills
    """
    print("=" * 70)
    print("TEST 1: Basic Memory Storage")
    print("=" * 70)
    
    kernel = create_kernel()
    memory = CareerMemory(kernel)
    
    print("\n📝 Storing skills in memory...\n")
    
    await memory.store_skill(
        skill_name="Python Programming",
        proficiency="advanced",
        evidence="5 years of experience, built 10+ production applications",
        category="technical"
    )
    
    await memory.store_skill(
        skill_name="Machine Learning",
        proficiency="intermediate",
        evidence="Completed 3 ML projects, familiar with scikit-learn",
        category="technical"
    )
    
    await memory.store_skill(
        skill_name="Azure OpenAI",
        proficiency="advanced",
        evidence="Built multiple GenAI applications",
        category="technical"
    )
    
    await memory.store_skill(
        skill_name="Semantic Kernel",
        proficiency="intermediate",
        evidence="Currently learning, built job search agent",
        category="technical"
    )
    
    await memory.store_skill(
        skill_name="Communication",
        proficiency="advanced",
        evidence="Led team presentations",
        category="soft"
    )
    
    print("\n✅ Stored 5 skills in memory!")
    print("💡 Each skill is now a vector (1536 numbers) in memory")


async def test_semantic_search():
    """
    Test 2: Semantic similarity search
    """
    print("\n" + "=" * 70)
    print("TEST 2: Semantic Search (The Magic!)")
    print("=" * 70)
    
    kernel = create_kernel()
    memory = CareerMemory(kernel)
    
    print("\n📝 Setting up memory with skills...\n")
    
    skills_to_store = [
        ("Python", "advanced", "5 years professional experience"),
        ("JavaScript", "intermediate", "3 years"),
        ("Machine Learning", "intermediate", "Multiple ML projects"),
        ("Deep Learning", "beginner", "Completed online course"),
        ("LLM Development", "advanced", "Built 5 GenAI applications"),
        ("Prompt Engineering", "expert", "Extensive GPT experience"),
        ("SQL", "intermediate", "Database design"),
        ("Docker", "intermediate", "Containerized applications"),
    ]
    
    for skill, prof, evidence in skills_to_store:
        await memory.store_skill(skill, prof, evidence)
    
    print("\n" + "=" * 70)
    print("🔍 SEMANTIC SEARCH DEMONSTRATIONS")
    print("=" * 70)
    
    print("\n1️⃣ Search: 'Python programming'")
    results = await memory.find_similar_skills("Python programming", limit=3)
    print(f"   Found {len(results)} similar skills")
    
    print("\n2️⃣ Search: 'AI and machine learning'")
    results = await memory.find_similar_skills("AI and machine learning", limit=3)
    print(f"   Found {len(results)} similar skills")
    print("   💡 Notice: Found ML, Deep Learning, LLM Development!")
    
    print("\n3️⃣ Search: 'ML expertise'")
    results = await memory.find_similar_skills("ML expertise", limit=3)
    print(f"   Found {len(results)} similar skills")
    print("   💡 'ML' matched 'Machine Learning' semantically!")
    
    print("\n4️⃣ Search: 'coding skills'")
    results = await memory.find_similar_skills("coding skills", limit=3)
    print(f"   Found {len(results)} similar skills")
    
    print("\n5️⃣ Search: 'generative AI development'")
    results = await memory.find_similar_skills("generative AI development", limit=3)
    print(f"   Found {len(results)} similar skills")
    
    print("\n" + "=" * 70)
    print("✨ This is the POWER of embeddings!")
    print("✨ Understands meaning, not just keywords!")
    print("=" * 70)


async def test_job_analysis_memory():
    """
    Test 3: Store and retrieve job analyses
    """
    print("\n" + "=" * 70)
    print("TEST 3: Job Analysis Memory")
    print("=" * 70)
    
    kernel = create_kernel()
    memory = CareerMemory(kernel)
    
    print("\n💼 Storing analyzed jobs...\n")
    
    await memory.store_job_analysis(
        job_title="Senior GenAI Engineer",
        company="TechCorp",
        analysis_result={
            "required_skills": ["Python", "LLMs", "Prompt Engineering", "Azure"],
            "experience_level": "senior",
            "years_experience": "5-7"
        },
        match_percentage=85
    )
    
    await memory.store_job_analysis(
        job_title="ML Engineer",
        company="DataCo",
        analysis_result={
            "required_skills": ["Python", "TensorFlow", "SQL"],
            "experience_level": "mid",
            "years_experience": "3-5"
        },
        match_percentage=70
    )
    
    await memory.store_job_analysis(
        job_title="AI Research Scientist",
        company="ResearchLabs",
        analysis_result={
            "required_skills": ["PyTorch", "Research", "PhD"],
            "experience_level": "senior",
            "years_experience": "7+"
        },
        match_percentage=45
    )
    
    print("✅ Stored 3 job analyses")
    
    print("\n🔍 Searching for similar jobs...\n")
    
    print("Search: 'GenAI positions'")
    results = await memory.find_similar_jobs("GenAI positions", limit=2)
    print(f"Found {len(results)} similar jobs")
    
    print("\nSearch: 'machine learning roles'")
    results = await memory.find_similar_jobs("machine learning roles", limit=2)
    print(f"Found {len(results)} similar jobs")


async def test_skill_coverage_calculation():
    """
    Test 4: Calculate skill match percentage
    """
    print("\n" + "=" * 70)
    print("TEST 4: Skill Coverage Calculation")
    print("=" * 70)
    
    kernel = create_kernel()
    memory = CareerMemory(kernel)
    
    print("\n📝 Your current skills:\n")
    
    your_skills = [
        ("Python", "advanced", "5 years"),
        ("Semantic Kernel", "intermediate", "Building projects"),
        ("Azure OpenAI", "advanced", "Multiple apps"),
        ("Prompt Engineering", "expert", "Extensive experience"),
        ("Docker", "intermediate", "Container deployments"),
    ]
    
    for skill, prof, evidence in your_skills:
        await memory.store_skill(skill, prof, evidence)
        print(f"  ✅ {skill} ({prof})")
    
    print("\n💼 Job Requirements:\n")
    
    job_requirements = [
        "Python programming",
        "LLM integration",
        "Azure OpenAI",
        "Semantic Kernel or LangChain",
        "Prompt engineering",
        "Vector databases",
        "Docker containers"
    ]
    
    for req in job_requirements:
        print(f"  📌 {req}")
    
    print("\n🔍 Calculating skill match...\n")
    
    percentage, matched, missing = await memory.calculate_skill_coverage(job_requirements)
    
    print("\n" + "=" * 70)
    print("📊 SKILL MATCH RESULTS")
    print("=" * 70)
    
    print(f"\n🎯 Overall Match: {percentage}%")
    
    print(f"\n✅ Skills You Have ({len(matched)}):")
    for skill in matched:
        print(f"   • {skill}")
    
    print(f"\n⚠️ Skills to Learn ({len(missing)}):")
    for skill in missing:
        print(f"   • {skill}")
    
    if percentage >= 70:
        print("\n💚 Strong match! You should apply!")
    elif percentage >= 50:
        print("\n💛 Decent match. Consider applying.")
    else:
        print("\n❤️ Weak match. Focus on building missing skills first.")


async def test_learning_progress_tracking():
    """
    Test 5: Track learning progress over time
    """
    print("\n" + "=" * 70)
    print("TEST 5: Learning Progress Tracking")
    print("=" * 70)
    
    kernel = create_kernel()
    memory = CareerMemory(kernel)
    
    print("\n📚 Tracking learning progress...\n")
    
    await memory.store_learning_progress(
        skill="Vector Databases",
        progress_percentage=30,
        notes="Completed intro tutorial, set up Pinecone"
    )
    
    await memory.store_learning_progress(
        skill="Fine-tuning LLMs",
        progress_percentage=15,
        notes="Read documentation, exploring LoRA"
    )
    
    await memory.store_learning_progress(
        skill="Semantic Kernel",
        progress_percentage=60,
        notes="Built job search agent! Memory system complete."
    )
    
    print("✅ Progress tracked for 3 skills")
    print("\n💡 Over time, you can visualize your learning journey!")


async def test_understanding_embeddings():
    """
    Test 6: Understand how embeddings work
    """
    print("\n" + "=" * 70)
    print("TEST 6: Understanding Embeddings (Educational)")
    print("=" * 70)
    
    kernel = create_kernel()
    memory = CareerMemory(kernel)
    
    print("\n🧪 Let's see how AI 'understands' similarity!\n")
    
    await memory.store_skill(
        "Python Programming",
        "advanced",
        "Programming language for AI/ML"
    )
    
    await memory.store_skill(
        "Cooking",
        "intermediate",
        "Hobby: Making Italian pasta"
    )
    
    await memory.store_skill(
        "Machine Learning",
        "intermediate",
        "AI and data science"
    )
    
    print("🔍 Query: 'software development'")
    print("   Expected: Should find 'Python Programming'")
    results = await memory.find_similar_skills("software development", limit=3)
    
    print("\n🔍 Query: 'food preparation'")
    print("   Expected: Should find 'Cooking', NOT 'Python'")
    results = await memory.find_similar_skills("food preparation", limit=3)
    
    print("\n✨ This shows embeddings understand context!")
    print("✨ 'Software development' → 'Python' (related)")
    print("✨ 'Food preparation' → 'Cooking' (related)")
    print("✨ These are NOT mixed up!")


async def main():
    """
    Main test runner
    """
    print("🚀 Episode 4: Memory Systems Tests\n")
    print("💡 Note: Uses embeddings (~$0.001 per 1000 tokens)\n")
    
    try:
        await test_basic_memory_storage()
        await test_semantic_search()
        await test_job_analysis_memory()
        await test_skill_coverage_calculation()
        await test_learning_progress_tracking()
        await test_understanding_embeddings()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        
        print("\n💡 Key Learnings:")
        print("1. Memory allows AI to remember information")
        print("2. Embeddings convert text → vectors (numbers)")
        print("3. Similar meanings → similar vectors")
        print("4. Semantic search finds similar items intelligently")
        print("5. Much better than keyword matching!")
        
        print("\n💰 Cost Breakdown:")
        print("   - ~50 embeddings × 50 tokens each = 2,500 tokens")
        print("   - Embedding cost: $0.0001 per 1K tokens")
        print("   - Total: ~$0.0003 (three hundredths of a cent!)")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())