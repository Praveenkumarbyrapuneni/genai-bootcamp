# src/agents/career_advisor.py

"""
Career Advisor Agent (Orchestrator)

This is the MAIN agent that coordinates all others.
It:
- Receives user requests
- Delegates to specialist agents
- Synthesizes their responses
- Provides final recommendations
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .market_researcher import MarketResearcherAgent
from .skills_coach import SkillsCoachAgent
from .application_strategist import ApplicationStrategistAgent


class CareerAdvisorAgent(BaseAgent):
    """
    Main orchestrator agent.
    
    What does it do?
    - Coordinates all other agents
    - Delegates tasks to specialists
    - Synthesizes multiple perspectives
    - Provides comprehensive advice
    
    Think of it as the team lead!
    """
    
    def __init__(self, kernel):
        """
        Initialize Career Advisor and all specialist agents.
        """
        super().__init__(
            name="Career Advisor",
            role="Career Strategy Orchestrator",
            expertise=[
                "Career strategy",
                "Team coordination",
                "Decision synthesis",
                "Comprehensive planning"
            ],
            kernel=kernel
        )
        
        # Create specialist agents
        self.market_researcher = MarketResearcherAgent(kernel)
        self.skills_coach = SkillsCoachAgent(kernel)
        self.application_strategist = ApplicationStrategistAgent(kernel)
        
        print(f"\n👥 Career Advisory Team assembled:")
        print(f"   • {self.market_researcher.name}")
        print(f"   • {self.skills_coach.name}")
        print(f"   • {self.application_strategist.name}")
        print(f"   • {self.name} (Orchestrator)")
    
    
    def get_system_prompt(self) -> str:
        """
        System prompt for career advisor.
        """
        return """
You are the Career Advisor, the lead coordinator of a career advisory team.

Your role:
- Coordinate specialist agents
- Synthesize multiple perspectives
- Provide comprehensive, actionable advice
- Make final recommendations
- Ensure all aspects are considered

You have access to:
- Market Researcher (job market insights)
- Skills Coach (skill development)
- Application Strategist (application tactics)

Your approach:
- Consider all specialist input
- Balance different perspectives
- Prioritize most impactful actions
- Provide clear, step-by-step guidance
- Be encouraging but realistic

When providing final advice:
- Summarize key insights from all agents
- Identify priorities
- Create actionable next steps
- Set realistic timelines
- Provide encouragement and motivation

You are supportive, strategic, and focused on results.
        """
    
    
    async def comprehensive_career_analysis(
        self,
        target_role: str,
        current_skills: List[str],
        target_companies: Optional[List[str]] = None,
        timeframe_months: int = 6
    ) -> Dict[str, str]:
        """
        Coordinate all agents for comprehensive analysis.
        
        This is the MAIN WORKFLOW - all agents collaborate!
        
        Args:
            target_role: Target job role
            current_skills: Current skills
            target_companies: Optional list of target companies
            timeframe_months: Time to job-ready
        
        Returns:
            Dictionary with all agents' insights
        """
        
        print("\n" + "=" * 70)
        print("🎯 COMPREHENSIVE CAREER ANALYSIS")
        print("=" * 70)
        print(f"\nTarget Role: {target_role}")
        print(f"Timeframe: {timeframe_months} months")
        print(f"Current Skills: {', '.join(current_skills[:5])}...")
        print("\n" + "=" * 70)
        
        results = {}
        
        # Step 1: Market Researcher analyzes demand
        print("\n📊 Phase 1: Market Research")
        print("-" * 70)
        
        market_analysis = await self.market_researcher.identify_trending_skills(target_role)
        results["market_research"] = market_analysis
        
        print(market_analysis[:300] + "...")
        
        # Step 2: Skills Coach assesses gaps
        print("\n\n🎓 Phase 2: Skills Assessment")
        print("-" * 70)
        
        # Extract required skills from market analysis (simplified)
        required_skills = [
            "Python", "LLMs", "Prompt Engineering", "Vector Databases",
            "Semantic Kernel", "Azure OpenAI", "Fine-tuning", "RAG Systems"
        ]
        
        skills_assessment = await self.skills_coach.assess_skill_level(
            current_skills,
            required_skills
        )
        results["skills_assessment"] = skills_assessment
        
        print(skills_assessment[:300] + "...")
        
        # Step 3: Skills Coach creates learning plan
        print("\n\n📚 Phase 3: Learning Plan")
        print("-" * 70)
        
        # Identify gaps (simplified - would parse from assessment)
        skill_gaps = ["Vector Databases", "Fine-tuning", "RAG Systems"]
        
        learning_plan = await self.skills_coach.create_learning_plan(
            skill_gaps,
            timeframe_weeks=timeframe_months * 4,
            current_level="intermediate"
        )
        results["learning_plan"] = learning_plan
        
        print(learning_plan[:300] + "...")
        
        # Step 4: Application Strategist provides strategy
        print("\n\n📝 Phase 4: Application Strategy")
        print("-" * 70)
        
        job_desc_sample = f"""
{target_role} position requiring:
- Strong Python skills
- LLM integration experience
- Prompt engineering
- Production deployment
        """
        
        candidate_bg = f"""
Current skills: {', '.join(current_skills)}
Working on: {', '.join(skill_gaps)}
        """
        
        app_strategy = await self.application_strategist.create_application_strategy(
            job_desc_sample,
            candidate_bg,
            match_percentage=75
        )
        results["application_strategy"] = app_strategy
        
        print(app_strategy[:300] + "...")
        
        # Step 5: Career Advisor synthesizes everything
        print("\n\n🎯 Phase 5: Final Synthesis")
        print("-" * 70)
        
        synthesis = await self._synthesize_recommendations(results, target_role, timeframe_months)
        results["final_recommendations"] = synthesis
        
        print(synthesis[:300] + "...")
        
        print("Results:", results)
        
        print("\n\n" + "=" * 70)
        print("✅ COMPREHENSIVE ANALYSIS COMPLETE")
        print("=" * 70)
        
        return results
    
    
    async def _synthesize_recommendations(
        self,
        agent_results: Dict[str, str],
        target_role: str,
        timeframe_months: int
    ) -> str:
        """
        Synthesize all agent inputs into final recommendations.
        
        Args:
            agent_results: Results from all specialist agents
            target_role: Target role
            timeframe_months: Timeframe
        
        Returns:
            Final synthesized recommendations
        """
        
        context = {
            "Market Researcher": agent_results.get("market_research", ""),
            "Skills Coach": agent_results.get("skills_assessment", "") + "\n" + agent_results.get("learning_plan", ""),
            "Application Strategist": agent_results.get("application_strategy", "")
        }
        
        query = f"""
Based on input from all specialist agents, provide final comprehensive recommendations.

Target: {target_role} in {timeframe_months} months

Synthesize insights and provide:
1. Overall Assessment (Are they ready? How close?)
2. Top 3 Priority Actions (most impactful)
3. Recommended Timeline
   - Months 1-2: Focus on...
   - Months 3-4: Focus on...
   - Months 5-6: Focus on...
4. Application Strategy
   - When to start applying
   - Which companies to target first
5. Success Metrics (how to track progress)
6. Motivational Message

Make it actionable, specific, and encouraging.
        """
        
        return await self.think(query, context)
    
    
    async def quick_job_evaluation(
        self,
        job_description: str,
        your_skills: List[str]
    ) -> str:
        """
        Quick evaluation of a specific job opportunity.
        
        Args:
            job_description: Job posting
            your_skills: Your current skills
        
        Returns:
            Quick evaluation and recommendation
        """
        
        print("\n🔍 Quick Job Evaluation")
        print("-" * 70)
        
        # Get strategist's opinion
        strategy = await self.application_strategist.create_application_strategy(
            job_description,
            f"Skills: {', '.join(your_skills)}",
            match_percentage=80  # Would calculate properly
        )
        
        # Synthesize recommendation
        query = f"""
Based on the application strategist's analysis, provide a quick recommendation.

Job Description:
{job_description[:200]}...

Should the candidate:
1. Apply immediately
2. Apply after some preparation
3. Skip this one

Provide:
- Quick verdict (Apply/Prepare/Skip)
- 3 key reasons
- If preparing, what to focus on
- Timeline recommendation

Keep it brief and actionable.
        """
        
        context = {"Application Strategist": strategy}
        
        return await self.think(query, context)