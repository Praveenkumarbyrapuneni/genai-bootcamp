# src/agents/market_researcher.py

"""
Market Researcher Agent

This agent specializes in:
- Analyzing job market trends
- Identifying in-demand skills
- Tracking salary ranges
- Finding emerging technologies
"""

from typing import Dict, List
from .base_agent import BaseAgent


class MarketResearcherAgent(BaseAgent):
    """
    Specialized agent for job market research.
    
    What does it do?
    - Analyzes job market data
    - Identifies trending skills
    - Reports on demand for roles
    - Provides market insights
    
    Think of it as your personal labor market analyst!
    """
    
    def __init__(self, kernel):
        """
        Initialize Market Researcher agent.
        """
        super().__init__(
            name="Market Researcher",
            role="Job Market Analyst",
            expertise=[
                "Labor market trends",
                "Skill demand analysis",
                "Salary research",
                "Emerging technologies",
                "Industry insights"
            ],
            kernel=kernel
        )
    
    
    def get_system_prompt(self) -> str:
        """
        System prompt for market researcher.
        """
        return """
You are the Market Researcher, an expert job market analyst specializing in GenAI and ML engineering roles.

Your expertise:
- Analyzing job market trends and demand
- Identifying most sought-after skills
- Tracking salary ranges and compensation
- Spotting emerging technologies and frameworks
- Understanding hiring patterns across companies

Your analysis style:
- Data-driven and objective
- Focus on actionable insights
- Provide specific examples
- Include recent trends (last 3-6 months)
- Highlight both current and emerging demands

When analyzing the market, consider:
- Geographic variations
- Company size differences (startup vs enterprise)
- Experience level requirements
- Industry-specific trends

Always provide concrete, actionable insights that help job seekers make informed decisions.
        """
    
    
    async def analyze_role_demand(self, role: str, location: str = "remote") -> str:
        """
        Analyze demand for a specific role.
        
        Args:
            role: Job role to analyze
            location: Geographic location or "remote"
        
        Returns:
            Market analysis
        """
        
        query = f"""
Analyze the current market demand for {role} positions in {location}.

Provide:
1. Overall demand level (high/medium/low)
2. Number of openings (estimate range)
3. Growth trend (increasing/stable/decreasing)
4. Key hiring companies
5. Typical salary ranges
6. Geographic hotspots

Be specific and data-oriented.
        """
        
        return await self.think(query)
    
    
    async def identify_trending_skills(self, role: str) -> str:
        """
        Identify trending skills for a role.
        
        Args:
            role: Target role
        
        Returns:
            Analysis of trending skills
        """
        
        query = f"""
Identify the most in-demand and trending skills for {role} positions.

Categorize as:
1. Core skills (must-have)
2. Highly desired skills (strong advantage)
3. Emerging skills (future-proofing)
4. Declining skills (becoming less relevant)

For each skill, explain:
- Why it's important
- How common it is in job postings
- How to learn it

Focus on technical skills, tools, and frameworks.
        """
        
        return await self.think(query)
    
    
    async def compare_role_opportunities(self, roles: List[str]) -> str:
        """
        Compare opportunities across multiple roles.
        
        Args:
            roles: List of roles to compare
        
        Returns:
            Comparative analysis
        """
        
        roles_str = ", ".join(roles)
        
        query = f"""
Compare market opportunities for these roles: {roles_str}

For each role, analyze:
1. Number of openings
2. Average salary range
3. Growth trajectory
4. Entry barriers (experience/education)
5. Career progression potential

Provide a clear comparison table and recommend which role offers:
- Most opportunities
- Best compensation
- Fastest growth
- Easiest entry

Help the job seeker make an informed choice.
        """
        
        return await self.think(query)