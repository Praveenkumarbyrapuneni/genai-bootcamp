# src/agents/market_researcher.py

"""
Market Researcher Agent - ROLE-SPECIFIC analysis
"""

from typing import Dict, List
from .base_agent import BaseAgent


class MarketResearcherAgent(BaseAgent):
    """
    Specialized agent for job market research.
    Provides ROLE-SPECIFIC insights, not generic AI advice.
    """
    
    def __init__(self, kernel):
        super().__init__(
            name="Market Researcher",
            role="Job Market Analyst",
            expertise=[
                "Labor market trends",
                "Skill demand analysis",
                "Salary research",
                "Industry insights"
            ],
            kernel=kernel
        )
    
    
    def get_system_prompt(self) -> str:
        return """
You are a BRUTALLY HONEST Market Researcher.

Your job:
- Analyze job market for SPECIFIC roles
- Give REAL salary data
- Be honest about competition
- Don't give AI/ML advice for non-AI roles

NEVER recommend RAG, Fine-tuning, Vector Databases unless the role SPECIFICALLY requires them.
        """
    
    
    async def analyze_role_specific(self, role: str, required_skills: List[str]) -> str:
        """
        Analyze market for a SPECIFIC role with its ACTUAL required skills.
        """
        
        query = f"""
Analyze the job market for: {role}

REQUIRED SKILLS FOR THIS ROLE (use ONLY these, not AI/ML skills unless listed):
{', '.join(required_skills)}

Provide:

## 📊 Market Analysis for {role}

### Demand Level
[High/Medium/Low and why]

### Salary Ranges (USD)
- Entry Level: $X - $Y
- Mid Level: $X - $Y  
- Senior Level: $X - $Y

### Competition Reality
[How competitive is this role? Be honest]

### Top Hiring Companies
[List 5-10 companies hiring for this SPECIFIC role]

### Skills Most Mentioned in Job Postings
[List the skills from the required skills list that appear most in postings]

### Geographic Hotspots
[Where are most jobs located?]

DO NOT mention RAG, LLMs, Vector Databases, Fine-tuning unless they are in the required skills list above.
        """
        
        return await self.think(query)
    
    
    async def identify_trending_skills(self, role: str) -> str:
        """Legacy method - kept for compatibility"""
        return await self.analyze_role_specific(role, [])