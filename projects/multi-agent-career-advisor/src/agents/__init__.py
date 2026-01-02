# src/agents/__init__.py

"""
Multi-Agent System

Specialized AI agents that collaborate on career development.
"""

from .base_agent import BaseAgent
from .market_researcher import MarketResearcherAgent
from .skills_coach import SkillsCoachAgent
from .application_strategist import ApplicationStrategistAgent
from .career_advisor import CareerAdvisorAgent

__all__ = [
    "BaseAgent",
    "MarketResearcherAgent",
    "SkillsCoachAgent",
    "ApplicationStrategistAgent",
    "CareerAdvisorAgent"
]