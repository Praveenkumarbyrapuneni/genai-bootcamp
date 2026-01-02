# episodes/ep05_planning/test_planner.py

"""
Episode 5: Testing Planning & Orchestration

This script demonstrates:
1. Sequential planning (linear multi-step plans)
2. Stepwise planning (adaptive thinking)
3. Automatic function selection
4. Plan execution
5. Real-world career planning scenarios
"""

import asyncio
import sys
import os

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.kernel_config import create_kernel
from src.plugins.job_intelligence import JobScraperPlugin, SkillsAnalyzerPlugin
from src.memory import CareerMemory
from src.planning import CareerPlanner


async def setup_kernel_with_plugins():
    """
    Set up kernel with all our plugins so planner can use them.
    The planner needs to know what functions are available!
    """
    print("🔧 Setting up kernel with all plugins...\n")
    
    # Create kernel
    kernel = create_kernel()
    
    # Add job scraper plugin (native functions)
    scraper = JobScraperPlugin()
    kernel.add_plugin(
        plugin=scraper,
        plugin_name="job_scraper"
    )
    print("✅ Added: Job Scraper Plugin")
    
    # Add skills analyzer plugin (semantic functions)
    analyzer = SkillsAnalyzerPlugin(kernel)
    kernel.add_plugin(
        plugin=analyzer,
        plugin_name="skills_analyzer"
    )
    print("✅ Added: Skills Analyzer Plugin")
    
    # Add memory (for skill storage and retrieval)
    memory = CareerMemory(kernel)
    
    print("\n📦 Available functions for planner:")
    
    # --- CORRECT WAY TO LIST FUNCTIONS IN SDK 1.0+ ---
    # We iterate over plugin items, then function items
    for plugin_name, plugin in kernel.plugins.items():
        print(f"\n   Plugin: {plugin_name}")
        for func_name, func in plugin.functions.items():
            print(f"      • {func_name}: {func.description}")
            
    return kernel, memory


async def test_simple_sequential_plan():
    """
    Test 1: Simple sequential plan
    Shows how planner creates a step-by-step plan.
    """
    print("\n" + "=" * 70)
    print("TEST 1: Simple Sequential Plan")
    print("=" * 70)
    
    kernel, memory = await setup_kernel_with_plugins()
    planner = CareerPlanner(kernel)
    
    print("\n🎯 Goal: Find and analyze GenAI jobs\n")
    
    # Simple goal for the planner
    goal = """
    Find recent GenAI engineering jobs and analyze the skills they require.
    Focus on remote positions.
    Provide a summary of the most common skills needed.
    """
    
    try:
        result = await planner.execute_custom_plan(goal)
        
        print("\n📊 Result:")
        print("=" * 70)
        print(result[:500])  # Show first 500 chars
        if len(result) > 500:
            print("... (truncated)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n⚠️ Note: {e}")
        import traceback
        traceback.print_exc()


async def test_job_preparation_plan():
    """
    Test 2: Create complete job preparation plan
    Planner figures out all steps needed to prepare for a job.
    """
    print("\n" + "=" * 70)
    print("TEST 2: Job Preparation Plan")
    print("=" * 70)
    
    kernel, memory = await setup_kernel_with_plugins()
    planner = CareerPlanner(kernel)
    
    # Store some skills in memory first
    print("\n📝 Storing your skills in memory...\n")
    await memory.store_skill("Python", "advanced", "5 years experience")
    await memory.store_skill("Azure OpenAI", "advanced", "Multiple projects")
    await memory.store_skill("Semantic Kernel", "intermediate", "Building agents")
    
    print("\n🎯 Creating preparation plan for GenAI Engineer role...\n")
    
    try:
        result = await planner.create_job_preparation_plan(
            job_title="Senior GenAI Engineer",
            company="TechCorp",
            your_current_skills=["Python", "Azure OpenAI", "Semantic Kernel"]
        )
        
        print("\n📋 Preparation Plan:")
        print("=" * 70)
        print(result[:600])
        if len(result) > 600:
            print("... (truncated)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n⚠️ Error: {e}")


async def test_learning_roadmap():
    """
    Test 3: Generate learning roadmap
    Uses stepwise planner for adaptive thinking.
    """
    print("\n" + "=" * 70)
    print("TEST 3: Learning Roadmap Creation")
    print("=" * 70)
    
    kernel, memory = await setup_kernel_with_plugins()
    planner = CareerPlanner(kernel)
    
    print("\n📚 Creating 12-week learning roadmap...\n")
    
    try:
        result = await planner.create_learning_roadmap(
            target_role="Senior GenAI Engineer",
            timeframe_weeks=12,
            current_level="intermediate"
        )
        
        print("\n📅 Learning Roadmap:")
        print("=" * 70)
        print(result[:600])
        if len(result) > 600:
            print("... (truncated)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n⚠️ Error: {e}")


async def test_market_analysis():
    """
    Test 4: Analyze job market trends
    Multi-step analysis plan.
    """
    print("\n" + "=" * 70)
    print("TEST 4: Job Market Analysis")
    print("=" * 70)
    
    kernel, memory = await setup_kernel_with_plugins()
    planner = CareerPlanner(kernel)
    
    print("\n📊 Analyzing GenAI engineer job market...\n")
    
    try:
        result = await planner.analyze_job_market_trends(
            role_type="GenAI Engineer",
            location="remote"
        )
        
        print("\n📈 Market Analysis:")
        print("=" * 70)
        print(result[:600])
        if len(result) > 600:
            print("... (truncated)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n⚠️ Error: {e}")


async def test_application_strategy():
    """
    Test 5: Create application strategy
    Strategic planning for job application.
    """
    print("\n" + "=" * 70)
    print("TEST 5: Application Strategy")
    print("=" * 70)
    
    kernel, memory = await setup_kernel_with_plugins()
    planner = CareerPlanner(kernel)
    
    job_desc = """
    Senior GenAI Engineer at InnovateCorp
    
    We're seeking an experienced GenAI engineer to build cutting-edge AI applications.
    
    Required:
    - 5+ years Python
    - LLM integration (GPT-4, Claude, Llama)
    - Prompt engineering expertise
    - Vector databases
    - Production ML deployment
    
    Preferred:
    - Azure OpenAI experience
    - Fine-tuning experience
    - Semantic Kernel or LangChain
    """
    
    your_background = """
    - 5 years Python development
    - Built 3 GenAI applications with Azure OpenAI
    - Expert in prompt engineering
    - Currently learning vector databases
    - Experience with Semantic Kernel
    - Deployed ML models with Docker
    """
    
    print("\n📝 Creating application strategy...\n")
    
    try:
        result = await planner.create_application_strategy(
            job_description=job_desc,
            your_background=your_background
        )
        
        print("\n💼 Application Strategy:")
        print("=" * 70)
        print(result[:600])
        if len(result) > 600:
            print("... (truncated)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n⚠️ Error: {e}")


async def demonstrate_planner_thinking():
    """
    Test 6: Show how planner thinks
    Educational demonstration.
    """
    print("\n" + "=" * 70)
    print("TEST 6: How Planners Think (Educational)")
    print("=" * 70)
    
    print("\n🧠 Understanding the Planner's Process:\n")
    
    print("1️⃣ USER GIVES GOAL:")
    print("   'Help me find the best GenAI job for my skills'\n")
    
    print("2️⃣ PLANNER LOOKS AT AVAILABLE FUNCTIONS:")
    print("   • job_scraper.scrape_genai_jobs")
    print("   • skills_analyzer.extract_skills_from_job")
    print("   • skills_analyzer.compare_skills_to_profile")
    print("   • memory.find_similar_skills (if wrapped)\n")
    
    print("3️⃣ PLANNER READS DESCRIPTIONS:")
    print("   • 'scrape_genai_jobs: Fetches recent GenAI jobs'")
    print("   • 'extract_skills: Analyzes job requirements'")
    print("   • 'compare_skills: Matches candidate to job'\n")
    
    print("4️⃣ PLANNER CREATES PLAN:")
    print("   Step 1: Call scrape_genai_jobs(keywords='GenAI', limit=10)")
    print("   Step 2: For each job, call extract_skills_from_job()")
    print("   Step 3: Call compare_skills_to_profile() for each")
    print("   Step 4: Rank jobs by match percentage")
    print("   Step 5: Return top 3 recommendations\n")
    
    print("5️⃣ PLANNER EXECUTES:")
    print("   ⚡ Running step 1... Done")
    print("   ⚡ Running step 2... Done")
    print("   ⚡ Running step 3... Done")
    print("   ⚡ Running step 4... Done")
    print("   ⚡ Running step 5... Done\n")
    
    print("6️⃣ RETURNS RESULTS:")
    print("   'Based on your skills, here are the top 3 matches...'\n")
    
    print("✨ THIS IS AUTONOMOUS AI!")
    print("✨ You give goal, AI figures out how to achieve it!")


async def main():
    """
    Main test runner
    """
    print("🚀 Episode 5: Planning & Orchestration Tests\n")
    print("💡 Note: Planning uses GPT-4o-mini to create plans (~$0.02 total)\n")
    
    try:
        await test_simple_sequential_plan()
        await test_job_preparation_plan()
        await test_learning_roadmap()
        await test_market_analysis()
        await test_application_strategy()
        await demonstrate_planner_thinking()
        
        print("\n" + "=" * 70)
        print("✅ ALL DEMONSTRATIONS COMPLETE!")
        print("=" * 70)
        
        print("\n💡 Key Learnings:")
        print("1. Planners break goals into steps automatically")
        print("2. Sequential Planner: Linear plans (A → B → C)")
        print("3. Stepwise Planner: Adaptive thinking")
        print("4. Planners read function descriptions to decide what to use")
        print("5. This enables true AI agent autonomy!")
        
        print("\n💰 Cost Estimate:")
        print("   - Plan creation: ~5 calls × 2000 tokens = $0.015")
        print("   - Plan execution: Varies by complexity")
        print("   - Total Episode 5: ~$0.02-0.05")
        
        print("\n🎯 What You Built:")
        print("   • AI that creates its own action plans")
        print("   • Autonomous task execution")
        print("   • Multi-step reasoning")
        print("   • Function selection and orchestration")
        
    except Exception as e:
        print(f"\n❌ Test note: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())