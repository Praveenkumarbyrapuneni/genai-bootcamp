# src/agents/skills_coach.py

"""
Skills Coach Agent - HONEST assessments, no sugar-coating
"""

from typing import Dict, List
from .base_agent import BaseAgent


class SkillsCoachAgent(BaseAgent):
    """
    Specialized agent for skill assessment and learning plans.
    Provides BRUTAL HONESTY about skill gaps.
    """
    
    def __init__(self, kernel):
        super().__init__(
            name="Skills Coach",
            role="Professional Development Specialist",
            expertise=[
                "Skill assessment",
                "Learning paths",
                "Certification guidance",
                "Competency mapping"
            ],
            kernel=kernel
        )
    
    
    def get_system_prompt(self) -> str:
        return """
You are a BRUTALLY HONEST Skills Coach.

Your job:
- Tell candidates EXACTLY what skills they're missing
- Don't say "you're doing great" if they're not
- Give realistic timelines for learning
- Be specific about what to learn and how

NEVER:
- Sugarcoat skill gaps
- Give generic learning advice
- Say someone is ready when they're not
        """
    
    
    async def honest_assessment(
        self,
        current_skills: List[str],
        required_skills: List[str],
        skill_gaps: List[str],
        matched_skills: List[str],
        readiness_score: int,
        target_role: str
    ) -> str:
        """
        Give an HONEST skill assessment.
        """
        
        query = f"""
Give a BRUTALLY HONEST skill assessment for someone targeting: {target_role}

THEIR SKILLS: {', '.join(current_skills) if current_skills else 'None provided'}

REQUIRED FOR {target_role.upper()}:
{', '.join(required_skills)}

SKILLS THEY HAVE: {', '.join(matched_skills) if matched_skills else 'NONE of the required skills'}
SKILLS MISSING: {', '.join(skill_gaps) if skill_gaps else 'None - fully qualified'}

READINESS: {readiness_score}%

Provide:

## 📋 Skill Assessment

### Reality Check
[If readiness is below 50%, say so clearly. Don't be nice about it.]

### Skills You Have That Matter
{chr(10).join(f"- ✅ {skill}" for skill in matched_skills) if matched_skills else "- ❌ None of the required skills"}

### Skills You're Missing (MUST LEARN)
{chr(10).join(f"- ❌ {skill}" for skill in skill_gaps) if skill_gaps else "- None"}

### Priority Order for Learning
[Rank the missing skills by importance - which to learn first]

### Honest Assessment
[Be direct: Are they close or far from being job-ready?]

DO NOT say they're "well-positioned" if readiness is below 60%.
        """
        
        return await self.think(query)
    
    
    async def create_realistic_plan(
        self,
        skill_gaps: List[str],
        timeframe: str,
        timeframe_months: int,
        target_role: str
    ) -> str:
        """
        Create a REALISTIC learning plan.
        """
        
        if not skill_gaps:
            return f"## ✅ No Learning Plan Needed\n\nYou already have all the required skills for {target_role}. Focus on interview prep and applying."
        
        query = f"""
Create a REALISTIC learning plan for {target_role}.

SKILLS TO LEARN: {', '.join(skill_gaps)}
TIMEFRAME GIVEN: {timeframe}

Is {timeframe} realistic to learn {len(skill_gaps)} skills? Be honest.

Provide:

## 📚 Learning Plan for {target_role}

### ⚠️ Timeline Reality Check
[Is {timeframe} enough time to learn {len(skill_gaps)} skills? If not, say so.]

### Realistic Timeline
[What's an HONEST estimate to become job-ready?]

### Learning Schedule

{"For each skill, provide:" if skill_gaps else ""}
{chr(10).join(f'''
#### {i+1}. {skill}
- **Time needed:** X weeks/months
- **Best resource:** [Specific course/book]
- **How to practice:** [Specific project idea]
- **How to prove it:** [Portfolio/certification]
''' for i, skill in enumerate(skill_gaps[:5]))}

### Weekly Time Commitment
[How many hours per week do they need to study?]

### Milestones
[What should they achieve by when?]

BE HONEST about whether their timeframe is realistic.
        """
        
        return await self.think(query)
    
    
    # Legacy methods for compatibility
    async def assess_skill_level(self, current_skills: List[str], required_skills: List[str]) -> str:
        skill_gaps = [s for s in required_skills if s.lower() not in [c.lower() for c in current_skills]]
        matched = [s for s in required_skills if s.lower() in [c.lower() for c in current_skills]]
        score = int((len(matched) / len(required_skills)) * 100) if required_skills else 0
        return await self.honest_assessment(current_skills, required_skills, skill_gaps, matched, score, "the role")
    
    async def create_learning_plan(self, skill_gaps: List[str], timeframe_weeks: int, current_level: str) -> str:
        return await self.create_realistic_plan(skill_gaps, f"{timeframe_weeks} weeks", timeframe_weeks // 4, "the role")