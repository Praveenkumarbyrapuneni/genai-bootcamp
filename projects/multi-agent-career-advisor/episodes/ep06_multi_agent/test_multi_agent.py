# episodes/ep07_multi_agent/test_multi_agent.py

import asyncio
import sys
import os
import time

# Add the src directory to Python's path so we can import our modules
# This gets the path to the 'careerpathai' root folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.kernel_config import create_kernel
from src.agents.career_advisor import CareerAdvisorAgent

async def run_multi_agent_system():
    """
    Runs the multi-agent career advisory system.
    """
    print("\n🎬 Episode 7: Initializing Multi-Agent System...")
    
    # 1. Setup the Kernel
    try:
        kernel = create_kernel()
    except Exception as e:
        print(f"❌ Failed to create kernel: {e}")
        return

    # 2. Initialize the Orchestrator (Career Advisor)
    # This automatically initializes the sub-agents (Researcher, Coach, Strategist)
    advisor = CareerAdvisorAgent(kernel)
    
    # 3. Define a Test User Profile
    # In a real app, this would come from a database or frontend input
    target_role = "Senior GenAI Engineer"
    current_skills = [
        "Python (Advanced)",
        "Basic SQL",
        "Git/GitHub",
        "REST APIs",
        "LangChain (Beginner)",
        "Docker (Basic)"
    ]
    timeframe_months = 6
    
    # 4. Run the Comprehensive Analysis
    # This triggers the chain: Researcher -> Coach -> Strategist -> Advisor Synthesis
    start_time = time.time()
    
    try:
        results = await advisor.comprehensive_career_analysis(
            target_role=target_role,
            current_skills=current_skills,
            timeframe_months=timeframe_months
        )
        
        # 5. Display Final Results Summary
        print("\n" + "="*50)
        print("📊 SYSTEM EXECUTION SUMMARY")
        print("="*50)
        
        print(f"⏱️ Total Execution Time: {time.time() - start_time:.2f} seconds")
        print(f"📂 Artifacts Generated: {len(results)} items")
        print("-" * 30)
        
        # We can access individual agent outputs from the results dict
        if "final_recommendations" in results:
            print("\n🏆 FINAL ADVISOR RECOMMENDATION:")
            print(results["final_recommendations"])
        else:
            print("❌ No final recommendations generated.")

    except Exception as e:
        print(f"\n❌ Error during multi-agent execution: {e}")
        import traceback
        traceback.print_exc()

    # 6. Bonus: Quick Job Evaluation Test
    # Demonstrating how to use just a specific part of the system
    print("\n" + "="*50)
    print("⚡ BONUS: Quick Job Evaluation")
    print("="*50)
    
    sample_job_post = """
    We are looking for a GenAI Engineer to build RAG pipelines. 
    Must have experience with Vector DBs (Pinecone/Qdrant) and Azure OpenAI.
    Remote, $150k-$180k.
    """
    
    quick_feedback = await advisor.quick_job_evaluation(
        job_description=sample_job_post,
        your_skills=current_skills
    )
    
    print(f"\n📝 Job Post: {sample_job_post.strip()}")
    print(f"\n🤖 Agent Verdict:\n{quick_feedback}")

if __name__ == "__main__":
    asyncio.run(run_multi_agent_system())