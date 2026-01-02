# src/agents/skills_coach.py

"""
Skills Coach Agent

This agent specializes in:
- Evaluating current skills
- Identifying skill gaps
- Creating learning plans
- Recommending resources
"""

from typing import Dict, List
from .base_agent import BaseAgent


class SkillsCoachAgent(BaseAgent):
    """
    Specialized agent for skill development.
    
    What does it do?
    - Evaluates your current skills
    - Identifies gaps for target roles
    - Creates personalized learning plans
    - Recommends courses and resources
    - Tracks learning progress
    
    Think of it as your personal career coach!
    """
    
    def __init__(self, kernel):
        """
        Initialize Skills Coach agent.
        """
        super().__init__(
            name="Skills Coach",
            role="Career Development Coach",
            expertise=[
                "Skill assessment",
                "Gap analysis",
                "Learning path design",
                "Resource recommendation",
                "Progress tracking",
                "Career development"
            ],
            kernel=kernel
        )
    
    
    def get_system_prompt(self) -> str:
        """
        System prompt for skills coach.
        """
        return """
You are the Skills Coach, an expert career development coach specializing in GenAI and ML engineering skill development.

Your expertise:
- Assessing current skill levels objectively
- Identifying skill gaps for target roles
- Creating realistic, achievable learning plans
- Recommending high-quality learning resources
- Providing motivation and encouragement
- Tracking progress and adjusting plans

Your coaching style:
- Supportive but honest
- Focus on practical, hands-on learning
- Prioritize skills that maximize job prospects
- Consider learner's current level and time constraints
- Emphasize building portfolio projects
- Encourage consistent, incremental progress

When creating learning plans:
- Break down into manageable steps
- Include mix of theory and practice
- Suggest specific projects to build
- Provide time estimates
- Include checkpoints and milestones

Always be encouraging while being realistic about effort required.
        """
    
    
    async def assess_skill_level(
        self,
        current_skills: List[str],
        required_skills: List[str]
    ) -> str:
        """
        Assess skill level and gaps.
        
        Args:
            current_skills: Skills the person has
            required_skills: Skills needed for target role
        
        Returns:
            Assessment and gap analysis
        """
        
        query = f"""
Assess the candidate's readiness for their target role.

Current Skills:
{chr(10).join(f"- {skill}" for skill in current_skills)}

Required Skills:
{chr(10).join(f"- {skill}" for skill in required_skills)}

Provide:
1. Overall readiness score (0-100%)
2. Skills they have (matched)
3. Skills they're missing (gaps)
4. Skills that are transferable/close
5. Priority order for learning missing skills
6. Estimated time to become job-ready

Be honest but encouraging. Focus on what they CAN do and what they NEED to learn.
        """
        
        return await self.think(query)
    
    
    async def create_learning_plan(
        self,
        skill_gaps: List[str],
        timeframe_weeks: int,
        current_level: str = "intermediate"
    ) -> str:
        """
        Create personalized learning plan.
        
        Args:
            skill_gaps: Skills to learn
            timeframe_weeks: Time available
            current_level: Current expertise level
        
        Returns:
            Detailed learning plan
        """
        
        query = f"""
Create a {timeframe_weeks}-week learning plan to master these skills:
{chr(10).join(f"- {skill}" for skill in skill_gaps)}

Learner's current level: {current_level}

Create a detailed plan with:
1. Week-by-week breakdown
2. For each week:
   - Specific skills/topics to focus on
   - Recommended resources (courses, tutorials, docs)
   - Practice projects to build
   - Time commitment (hours/week)
   - Completion criteria

3. Major milestones at weeks 4, 8, 12 (if applicable)
4. Portfolio projects to showcase skills
5. How to demonstrate mastery

Make it practical, achievable, and focused on landing a job.
        """
        
        return await self.think(query)
    
    
    async def recommend_resources(self, skill: str, learning_style: str = "hands-on") -> str:
        """
        Recommend learning resources for a skill.
        
        Args:
            skill: Skill to learn
            learning_style: Preferred learning style
        
        Returns:
            Curated resource recommendations
        """
        
        query = f"""
Recommend the best learning resources for: {skill}

Learner prefers: {learning_style} learning

Provide:
1. Top 3 courses/tutorials (with URLs if known)
2. Essential documentation/guides
3. Practice projects (beginner to advanced)
4. Communities/forums for help
5. Books/papers (if relevant)
6. YouTube channels/playlists

Prioritize:
- Free or affordable options
- High-quality, up-to-date content
- Practical, project-based learning
- Resources that lead to portfolio pieces

Explain WHY each resource is recommended.
        """
        
        return await self.think(query)