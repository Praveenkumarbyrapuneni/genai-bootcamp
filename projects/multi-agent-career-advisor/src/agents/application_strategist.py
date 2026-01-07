# src/agents/application_strategist.py

"""
Application Strategist Agent - HONEST job application advice
"""

from typing import Dict, List
from .base_agent import BaseAgent


class ApplicationStrategistAgent(BaseAgent):
    """
    Specialized agent for job application strategy.
    Provides HONEST advice about when to apply.
    """
    
    def __init__(self, kernel):
        super().__init__(
            name="Application Strategist",
            role="Job Application Specialist",
            expertise=[
                "Resume optimization",
                "Interview preparation",
                "Application timing",
                "Company targeting"
            ],
            kernel=kernel
        )
    
    
    def get_system_prompt(self) -> str:
        return """
You are a BRUTALLY HONEST Application Strategist.

Your job:
- Tell candidates when they're NOT ready to apply
- Don't encourage applying if they'll just get rejected
- Give honest feedback about their chances
- Help them understand what recruiters actually look for

NEVER:
- Say "apply now" if they're missing key skills
- Give false hope about callback rates
- Sugarcoat their chances
        """
    
    
    async def honest_strategy(
        self,
        target_role: str,
        readiness_score: int,
        skill_gaps: List[str],
        matched_skills: List[str],
        timeframe: str
    ) -> str:
        """
        Give HONEST application strategy.
        """
        
        should_apply = readiness_score >= 60
        
        query = f"""
Give BRUTALLY HONEST application advice for {target_role}.

READINESS SCORE: {readiness_score}%
SKILLS THEY HAVE: {', '.join(matched_skills) if matched_skills else 'None relevant'}
SKILLS MISSING: {', '.join(skill_gaps) if skill_gaps else 'None'}
THEIR TIMEFRAME: {timeframe}

Provide:

## 📝 Application Strategy

### Should You Apply Now?
{"⚠️ NO - You're not ready yet." if readiness_score < 50 else "⚡ Maybe - But expect low callback rates." if readiness_score < 70 else "✅ Yes - You have a reasonable chance."}

### Your Realistic Callback Rate
[Based on {readiness_score}% readiness, what % of applications will get callbacks? Be honest.]

### What Recruiters Will See
[When they look at your resume, what's missing that will get you rejected?]

### When to Start Applying
{"Wait until you've learned: " + ', '.join(skill_gaps[:3]) if readiness_score < 50 else "Start applying to practice, but focus on learning" if readiness_score < 70 else "Start applying now"}

### Application Priority
1. **Apply Now:** [Types of companies/roles if any]
2. **Apply After Learning:** [What to learn first]
3. **Reach Companies:** [Companies to target later]

### Resume Red Flags
[What will make recruiters skip your resume?]

### Interview Reality
[If you get an interview, what questions will expose your gaps?]

DO NOT be encouraging if readiness is below 50%. Be direct about their low chances.
        """
        
        return await self.think(query)
    
    
    # Legacy method for compatibility
    async def create_application_strategy(self, job_description: str, candidate_background: str, match_percentage: int) -> str:
        return await self.honest_strategy(
            target_role="the role",
            readiness_score=match_percentage,
            skill_gaps=[],
            matched_skills=[],
            timeframe="6 months"
        )