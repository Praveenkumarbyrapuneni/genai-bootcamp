# src/agents/career_advisor.py

"""
Career Advisor Agent (Orchestrator)

This is the MAIN agent that coordinates all others.
It:
- Receives user requests
- Delegates to specialist agents
- Synthesizes their responses
- Provides final recommendations with BRUTAL HONESTY
- DEEPLY ANALYZES resumes like ChatGPT
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent
from .market_researcher import MarketResearcherAgent
from .skills_coach import SkillsCoachAgent
from .application_strategist import ApplicationStrategistAgent


# Role-specific required skills mapping
ROLE_SKILLS_MAP = {
    "data analyst": [
        "SQL", "Excel", "Python", "Tableau", "Power BI", 
        "Statistics", "Data Visualization", "ETL", "Data Cleaning",
        "Business Intelligence", "A/B Testing", "Reporting"
    ],
    "data analysis": [
        "SQL", "Excel", "Python", "Tableau", "Power BI", 
        "Statistics", "Data Visualization", "ETL", "Data Cleaning",
        "Business Intelligence", "A/B Testing", "Reporting"
    ],
    "data scientist": [
        "Python", "Machine Learning", "Statistics", "SQL", "Pandas",
        "Scikit-learn", "Deep Learning", "Data Visualization", 
        "Feature Engineering", "Model Deployment", "A/B Testing"
    ],
    "machine learning engineer": [
        "Python", "TensorFlow", "PyTorch", "MLOps", "Docker",
        "Kubernetes", "Model Deployment", "Feature Engineering",
        "Deep Learning", "SQL", "Cloud Platforms"
    ],
    "ml engineer": [
        "Python", "TensorFlow", "PyTorch", "MLOps", "Docker",
        "Kubernetes", "Model Deployment", "Feature Engineering",
        "Deep Learning", "SQL", "Cloud Platforms"
    ],
    "genai engineer": [
        "Python", "LLMs", "Prompt Engineering", "RAG Systems",
        "Vector Databases", "LangChain", "Semantic Kernel", 
        "Fine-tuning", "Azure OpenAI", "API Development"
    ],
    "ai engineer": [
        "Python", "LLMs", "Prompt Engineering", "RAG Systems",
        "Vector Databases", "LangChain", "Deep Learning",
        "Fine-tuning", "Cloud Platforms", "API Development"
    ],
    "software engineer": [
        "Data Structures", "Algorithms", "System Design", "Git",
        "SQL", "APIs", "Testing", "CI/CD", "Problem Solving",
        "Code Review", "Documentation"
    ],
    "sde": [
        "Data Structures", "Algorithms", "System Design", "Git",
        "SQL", "APIs", "Testing", "CI/CD", "Problem Solving",
        "Code Review", "Documentation"
    ],
    "software developer": [
        "Data Structures", "Algorithms", "System Design", "Git",
        "SQL", "APIs", "Testing", "CI/CD", "Problem Solving",
        "Code Review", "Documentation"
    ],
    "frontend developer": [
        "HTML", "CSS", "JavaScript", "React", "TypeScript",
        "Responsive Design", "Git", "APIs", "Testing", "UI/UX"
    ],
    "backend developer": [
        "Python", "Node.js", "SQL", "APIs", "System Design",
        "Database Design", "Caching", "Security", "Docker", "Git"
    ],
    "devops engineer": [
        "Linux", "Docker", "Kubernetes", "CI/CD", "AWS/Azure/GCP",
        "Terraform", "Monitoring", "Scripting", "Networking", "Security"
    ],
    "product manager": [
        "Product Strategy", "User Research", "Roadmapping", "Agile",
        "Data Analysis", "Stakeholder Management", "Prioritization",
        "A/B Testing", "Communication", "Market Analysis"
    ],
    "default": [
        "Problem Solving", "Communication", "Teamwork", "Adaptability",
        "Technical Skills", "Domain Knowledge", "Project Management"
    ]
}


def get_required_skills_for_role(role: str) -> List[str]:
    """Get the required skills for a specific role."""
    role_lower = role.lower().strip()
    
    # Check for exact match first
    if role_lower in ROLE_SKILLS_MAP:
        return ROLE_SKILLS_MAP[role_lower]
    
    # Check for partial match
    for key in ROLE_SKILLS_MAP:
        if key in role_lower or role_lower in key:
            return ROLE_SKILLS_MAP[key]
    
    # Return default if no match
    return ROLE_SKILLS_MAP["default"]


def calculate_readiness_score(current_skills: List[str], required_skills: List[str]) -> int:
    """Calculate actual readiness percentage based on skill match."""
    if not required_skills:
        return 0
    
    current_lower = [s.lower().strip() for s in current_skills]
    required_lower = [s.lower().strip() for s in required_skills]
    
    matched = sum(1 for skill in required_lower if any(
        skill in curr or curr in skill for curr in current_lower
    ))
    
    return int((matched / len(required_skills)) * 100)


class CareerAdvisorAgent(BaseAgent):
    """
    Main orchestrator agent with BRUTAL HONESTY.
    
    Analyzes FULL resumes - experience, projects, education, everything.
    Just like ChatGPT would.
    """
    
    def __init__(self, kernel):
        super().__init__(
            name="Career Advisor",
            role="Career Strategy Orchestrator & Resume Analyst",
            expertise=[
                "Career strategy",
                "Resume deep analysis",
                "Experience evaluation",
                "Project assessment",
                "Team coordination", 
                "Decision synthesis",
                "Comprehensive planning"
            ],
            kernel=kernel
        )
        
        self.market_researcher = MarketResearcherAgent(kernel)
        self.skills_coach = SkillsCoachAgent(kernel)
        self.application_strategist = ApplicationStrategistAgent(kernel)
    
    
    def get_system_prompt(self) -> str:
        return """
You are a BRUTALLY HONEST Career Advisor and Resume Analyst. You DO NOT sugarcoat anything.

When given a resume, you MUST:
1. READ THE ENTIRE RESUME carefully - every word matters
2. Analyze their WORK EXPERIENCE - what did they actually do? How long? What impact?
3. Evaluate their PROJECTS - are they relevant? Complex enough? Impressive?
4. Check their EDUCATION - is it sufficient for the role?
5. Look at their ACHIEVEMENTS - any quantified results? Awards? Certifications?
6. Identify GAPS - missing experience, short tenures, skill gaps

Your approach:
- Give REALITY CHECKS, not motivational speeches
- If their experience is weak, say so
- If their projects are too basic, tell them
- If they need more years of experience, be direct
- Calculate REAL readiness based on their FULL background
- Compare their profile to what companies ACTUALLY want

NEVER:
- Ignore the resume content
- Give generic advice that doesn't reference their specific background
- Say "great experience" if it's mediocre
- Recommend things they've clearly already done

ALWAYS:
- Quote specific parts of their resume
- Point out specific weaknesses in their experience
- Suggest specific improvements to their projects
- Give honest timeline based on their current level
        """
    
    
    async def analyze_resume_deeply(self, resume_text: str, target_role: str) -> Dict[str, any]:
        """
        Deeply analyze a resume like ChatGPT would.
        Extract experience, projects, education, and assess quality.
        """
        
        analysis_prompt = f"""
Analyze this resume DEEPLY for a {target_role} position. Read EVERY line carefully.

RESUME:
---
{resume_text}
---

Provide a detailed JSON-style analysis:

1. EXPERIENCE ANALYSIS:
   - Total years of experience
   - Relevant experience for {target_role}
   - Companies worked at (tier: FAANG/Big Tech/Startup/Other)
   - Key responsibilities
   - Quantified achievements (numbers, percentages, impact)
   - Gaps or red flags (short tenures, gaps, unrelated roles)

2. PROJECTS ANALYSIS:
   - List each project mentioned
   - For each: Is it relevant to {target_role}? How complex? Impressive?
   - Missing project types they should add
   - Project improvement suggestions

3. SKILLS EXTRACTED:
   - Technical skills found
   - Soft skills found
   - Certifications
   - Missing critical skills for {target_role}

4. EDUCATION:
   - Degree and field
   - University tier
   - Relevant coursework
   - Is it sufficient for {target_role}?

5. OVERALL ASSESSMENT:
   - Strengths (be specific, quote from resume)
   - Weaknesses (be brutally honest)
   - Readiness score for {target_role} (0-100%)
   - Experience level (Entry/Mid/Senior)
   - Competitive rating vs other candidates (Low/Medium/High)

Be SPECIFIC. Quote from the resume. Don't be generic.
        """
        
        analysis = await self.think(analysis_prompt, {})
        return {"raw_analysis": analysis}
    
    
    async def comprehensive_career_analysis(
        self,
        target_role: str,
        current_skills: List[str],
        target_companies: Optional[List[str]] = None,
        timeframe_months: int = 6,
        timeframe_display: Optional[str] = None,
        resume_text: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Coordinate all agents for comprehensive analysis.
        If resume is provided, do DEEP analysis like ChatGPT.
        """
        
        # Get role-specific required skills
        required_skills = get_required_skills_for_role(target_role)
        
        timeframe_str = timeframe_display or f"{timeframe_months} months"
        
        results = {}
        
        # If resume is provided, do DEEP ANALYSIS first
        resume_analysis = None
        if resume_text and len(resume_text.strip()) > 100:
            resume_analysis = await self.analyze_resume_deeply(resume_text, target_role)
            
            # Create resume-based reality check
            results["final_recommendations"] = await self._create_resume_based_analysis(
                resume_text=resume_text,
                target_role=target_role,
                timeframe=timeframe_str,
                required_skills=required_skills
            )
            
            results["market_research"] = await self._create_market_fit_analysis(
                resume_text=resume_text,
                target_role=target_role,
                required_skills=required_skills
            )
            
            results["learning_plan"] = await self._create_personalized_learning_plan(
                resume_text=resume_text,
                target_role=target_role,
                timeframe=timeframe_str,
                timeframe_months=timeframe_months
            )
            
            results["application_strategy"] = await self._create_application_readiness(
                resume_text=resume_text,
                target_role=target_role,
                timeframe=timeframe_str
            )
        else:
            # No resume - use skills-based analysis
            readiness_score = calculate_readiness_score(current_skills, required_skills)
            
            current_lower = [s.lower().strip() for s in current_skills]
            skill_gaps = [
                skill for skill in required_skills 
                if not any(skill.lower() in curr or curr in skill.lower() for curr in current_lower)
            ]
            matched_skills = [
                skill for skill in required_skills 
                if any(skill.lower() in curr or curr in skill.lower() for curr in current_lower)
            ]
            
            # Use existing skills-based methods
            results["market_research"] = await self.market_researcher.analyze_role_specific(
                target_role, required_skills
            )
            
            results["learning_plan"] = await self.skills_coach.create_realistic_plan(
                skill_gaps=skill_gaps,
                timeframe=timeframe_str,
                timeframe_months=timeframe_months,
                target_role=target_role
            )
            
            results["application_strategy"] = await self.application_strategist.honest_strategy(
                target_role=target_role,
                readiness_score=readiness_score,
                skill_gaps=skill_gaps,
                matched_skills=matched_skills,
                timeframe=timeframe_str
            )
            
            results["final_recommendations"] = await self._create_skills_based_reality_check(
                target_role=target_role,
                current_skills=current_skills,
                required_skills=required_skills,
                skill_gaps=skill_gaps,
                matched_skills=matched_skills,
                readiness_score=readiness_score,
                timeframe=timeframe_str
            )
        
        return results
    
    
    async def _create_resume_based_analysis(
        self,
        resume_text: str,
        target_role: str,
        timeframe: str,
        required_skills: List[str]
    ) -> str:
        """Create a DEEP resume-based analysis like ChatGPT using Groq for speed."""
        
        from src.groq_client import get_groq_client
        
        groq_client = get_groq_client()
        
        system_prompt = """You are a BRUTALLY HONEST Career Advisor. You analyze resumes deeply and give reality checks, not motivational speeches. Be specific, quote from resumes, and be direct about weaknesses."""
        
        user_prompt = f"""Analyze this resume for {target_role} in {timeframe}.

RESUME:
---
{resume_text[:3000]}
---

REQUIRED SKILLS: {', '.join(required_skills)}

Give a BRUTALLY HONEST analysis with:
1. What you found in their resume (experience, projects, education, skills)
2. Readiness score (0-100%)
3. Strengths and weaknesses (be specific)
4. Is {timeframe} realistic?
5. Specific action items

Be direct and honest."""
        
        return await groq_client.get_completion(user_prompt, system_prompt, max_tokens=3000)
    
    
    async def _create_market_fit_analysis(
        self,
        resume_text: str,
        target_role: str,
        required_skills: List[str]
    ) -> str:
        """Analyze how the candidate fits the market based on their resume using Groq."""
        
        from src.groq_client import get_groq_client
        
        groq_client = get_groq_client()
        
        system_prompt = """You are a career market analyst. Analyze how candidates compare to market requirements and be honest about their competitive position."""
        
        user_prompt = f"""Analyze market fit for {target_role}.

RESUME:
---
{resume_text[:2000]}
---

REQUIRED SKILLS: {', '.join(required_skills)}

Provide:
1. How they compare to other candidates
2. What recruiters want vs what they have (experience, projects, skills, education)
3. Companies they could target (FAANG, Big Tech, Mid-size, Startups)
4. Their competitive position
5. Realistic salary expectations

Be honest and specific."""
        
        return await groq_client.get_completion(user_prompt, system_prompt, max_tokens=2000)
    
    
    async def _create_personalized_learning_plan(
        self,
        resume_text: str,
        target_role: str,
        timeframe: str,
        timeframe_months: int
    ) -> str:
        """Create a learning plan based on resume gaps using Groq."""
        
        from src.groq_client import get_groq_client
        
        groq_client = get_groq_client()
        
        system_prompt = """You are a learning plan expert. Create personalized, actionable learning paths based on resume gaps."""
        
        user_prompt = f"""Create a learning plan for {target_role} in {timeframe}.

RESUME:
---
{resume_text[:2000]}
---

Based on their resume:
1. What they already know (don't make them relearn)
2. What they need to learn (gaps)
3. Priority learning path (Phase 1, 2, 3)
4. Specific projects to build
5. Weekly time commitment
6. Is {timeframe} realistic?

Be specific to their gaps."""
        
        return await groq_client.get_completion(user_prompt, system_prompt, max_tokens=2500)
    
    
    async def _create_application_readiness(
        self,
        resume_text: str,
        target_role: str,
        timeframe: str
    ) -> str:
        """Assess application readiness based on resume using Groq."""
        
        from src.groq_client import get_groq_client
        
        groq_client = get_groq_client()
        
        system_prompt = """You are an application readiness coach. Assess if candidates are ready to apply and give honest feedback on their resume."""
        
        user_prompt = f"""Assess application readiness for {target_role}.

RESUME:
---
{resume_text[:2000]}
---

Provide:
1. Should they apply now? (Yes/No/Maybe - why)
2. Resume strengths (keep these)
3. Resume weaknesses (fix these)
4. Resume improvement suggestions
5. Interview readiness (what they'll struggle with)
6. When to start applying
7. Callback rate prediction
8. Priority action plan

Be honest based on their resume."""
        
        return await groq_client.get_completion(user_prompt, system_prompt, max_tokens=2000)
    
    
    async def _create_skills_based_reality_check(
        self,
        target_role: str,
        current_skills: List[str],
        required_skills: List[str],
        skill_gaps: List[str],
        matched_skills: List[str],
        readiness_score: int,
        timeframe: str
    ) -> str:
        """Create reality check based on skills only (no resume) using Groq."""
        
        from src.groq_client import get_groq_client
        
        groq_client = get_groq_client()
        
        system_prompt = """You are a career advisor. Give honest reality checks based on skills."""
        
        user_prompt = f"""Reality check for {target_role} in {timeframe}.

NOTE: No resume provided - skills-based analysis only.

THEIR SKILLS: {', '.join(current_skills) if current_skills else 'None'}
REQUIRED: {', '.join(required_skills)}
MATCHED: {', '.join(matched_skills) if matched_skills else 'None'}
MISSING: {', '.join(skill_gaps) if skill_gaps else 'None'}
READINESS: {readiness_score}%

Provide:
1. Readiness explanation
2. Skills they have vs need
3. Is {timeframe} realistic?
4. What they need to do
5. Honest bottom line

Remind them to upload resume for better analysis."""
        
        return await groq_client.get_completion(user_prompt, system_prompt, max_tokens=1500)