# src/agents/application_strategist.py

"""
Application Strategist Agent

This agent specializes in:
- Job application strategy
- Resume optimization
- Cover letter guidance
- Interview preparation
- Application timing
"""

from typing import Dict, List
from .base_agent import BaseAgent


class ApplicationStrategistAgent(BaseAgent):
    """
    Specialized agent for job application strategy.
    
    What does it do?
    - Plans application approach
    - Optimizes resumes for specific jobs
    - Drafts cover letter points
    - Prepares for interviews
    - Tracks applications
    
    Think of it as your application expert!
    """
    
    def __init__(self, kernel):
        """
        Initialize Application Strategist agent.
        """
        super().__init__(
            name="Application Strategist",
            role="Job Application Expert",
            expertise=[
                "Resume optimization",
                "Cover letter writing",
                "Interview preparation",
                "Application strategy",
                "ATS systems",
                "Networking tactics"
            ],
            kernel=kernel
        )
    
    
    def get_system_prompt(self) -> str:
        """
        System prompt for application strategist.
        """
        return """
You are the Application Strategist, an expert in job application strategy and career advancement.

Your expertise:
- Resume optimization for ATS systems
- Tailoring applications to specific roles
- Cover letter best practices
- Interview preparation and coaching
- Strategic timing of applications
- Networking and referral strategies
- Follow-up tactics

Your strategic approach:
- Maximize chances of getting interviews
- Emphasize relevant experience
- Address potential concerns proactively
- Position candidate competitively
- Provide specific, actionable advice
- Focus on both short-term wins and long-term career

When advising on applications:
- Tailor advice to the specific job
- Consider company culture and values
- Suggest concrete examples to use
- Anticipate interviewer questions
- Recommend preparation activities

Always be practical, specific, and focused on getting results.
        """
    
    
    async def create_application_strategy(
        self,
        job_description: str,
        candidate_background: str,
        match_percentage: int
    ) -> str:
        """
        Create application strategy for a specific job.
        
        Args:
            job_description: Full job posting
            candidate_background: Candidate's experience
            match_percentage: Skill match score
        
        Returns:
            Detailed application strategy
        """
        
        query = f"""
Create a strategic application plan for this job.

Job Description:
{job_description}

Candidate Background:
{candidate_background}

Skill Match: {match_percentage}%

Provide:
1. Should they apply? (Yes/Maybe/Wait)
2. Application timing recommendation
3. Resume highlights (what to emphasize)
4. Experience to feature prominently
5. Skills to highlight
6. Gaps/weaknesses and how to address them
7. Cover letter key points (3-5 bullets)
8. Networking opportunities (if any)
9. Interview preparation focus areas
10. Questions to prepare for

Be strategic and specific. Focus on maximizing interview chances.
        """
        
        return await self.think(query)
    
    
    async def optimize_resume_section(
        self,
        original_text: str,
        job_requirements: str
    ) -> str:
        """
        Optimize resume section for specific job.
        
        Args:
            original_text: Current resume text
            job_requirements: Target job requirements
        
        Returns:
            Optimized resume suggestions
        """
        
        query = f"""
Optimize this resume section for the target job.

Original Text:
{original_text}

Job Requirements:
{job_requirements}

Provide:
1. Optimized version of the text
2. Keywords to include (for ATS)
3. Specific accomplishments to add
4. Metrics/numbers to include
5. What to remove or de-emphasize

Make it compelling, specific, and keyword-rich while staying truthful.
        """
        
        return await self.think(query)
    
    
    async def prepare_interview_questions(
        self,
        job_title: str,
        company: str,
        job_description: str
    ) -> str:
        """
        Generate likely interview questions.
        
        Args:
            job_title: Position title
            company: Company name
            job_description: Full job posting
        
        Returns:
            Interview preparation guide
        """
        
        query = f"""
Prepare interview questions for: {job_title} at {company}

Job Description:
{job_description}

Provide:
1. 10 likely technical questions
2. 5 behavioral questions
3. 3 company-specific questions
4. Questions about the role/team
5. For each question:
   - Why they ask it
   - How to structure your answer
   - Key points to include

Also suggest:
- Questions to ask the interviewer
- Red flags to watch for
- How to demonstrate your value

Make it comprehensive and actionable.
        """
        
        return await self.think(query)