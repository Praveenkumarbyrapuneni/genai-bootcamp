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
        """Create a DEEP resume-based analysis like ChatGPT."""
        
        prompt = f"""
You are analyzing a resume for someone who wants to become a {target_role} in {timeframe}.

READ THIS RESUME CAREFULLY - EVERY WORD:
---
{resume_text}
---

REQUIRED SKILLS FOR {target_role.upper()}:
{', '.join(required_skills)}

Now give a BRUTALLY HONEST analysis. Structure your response EXACTLY like this:

## 🔍 DEEP RESUME ANALYSIS

### 📋 What I Found in Your Resume:

**Work Experience:**
[Summarize their experience. How many years? What companies? What did they ACTUALLY do?]

**Projects:**
[List their projects. Are they impressive? Relevant? Complex enough?]

**Education:**
[Their degree, university. Is it sufficient?]

**Skills Mentioned:**
[What skills did you find in their resume?]

---

## 🚨 REALITY CHECK for {target_role}

### Your Readiness Score: [X]%
[Calculate based on their FULL resume - experience + projects + skills + education]

### ✅ What's Working FOR You:
[List specific strengths FROM their resume - quote specific experience/projects]
- [Strength 1 - be specific, reference their resume]
- [Strength 2]
- [Strength 3]

### ❌ What's Working AGAINST You:
[Be brutally honest about weaknesses]
- [Weakness 1 - missing experience, weak projects, etc.]
- [Weakness 2]
- [Weakness 3]

### 🎯 Experience Gap Analysis:
[Compare their experience to what {target_role} positions typically require]
- Years of experience needed vs what they have
- Type of experience needed vs what they have
- Missing domain knowledge

### 📊 Project Assessment:
[Evaluate their projects specifically]
- Are their projects complex enough for {target_role}?
- What types of projects are they missing?
- Specific project ideas they should build

### ⏰ Is {timeframe} Realistic?
[Based on their CURRENT resume, can they be ready in {timeframe}?]

### 📋 Specific Action Items:
[NOT generic advice - specific to THEIR resume]
1. [Action 1 - reference what they're missing]
2. [Action 2]
3. [Action 3]
4. [Action 4]
5. [Action 5]

### 💡 Bottom Line:
[One paragraph of brutal honesty. Reference their specific background. Don't be generic.]

IMPORTANT:
- Quote specific things from their resume
- Don't give generic advice
- Be honest about their weaknesses
- Compare to what recruiters actually want
        """
        
        return await self.think(prompt, {})
    
    
    async def _create_market_fit_analysis(
        self,
        resume_text: str,
        target_role: str,
        required_skills: List[str]
    ) -> str:
        """Analyze how the candidate fits the market based on their resume."""
        
        prompt = f"""
Analyze how this candidate's resume compares to market requirements for {target_role}.

RESUME:
---
{resume_text}
---

REQUIRED SKILLS FOR {target_role}:
{', '.join(required_skills)}

Provide:

## 📊 Market Fit Analysis

### How You Compare to Other Candidates:
[Based on their resume, how do they stack up?]

### What Recruiters Look For vs What You Have:

| Requirement | What Recruiters Want | What You Have | Gap |
|-------------|---------------------|---------------|-----|
| Experience | [X years] | [Their years] | [Gap] |
| Projects | [Type needed] | [Their projects] | [Gap] |
| Skills | [Key skills] | [Their skills] | [Gap] |
| Education | [Typical requirement] | [Their education] | [Gap] |

### Companies You Could Target:
[Based on their current profile]
- Tier 1 (FAANG): [Ready/Not Ready - why]
- Tier 2 (Big Tech): [Ready/Not Ready - why]
- Tier 3 (Mid-size): [Ready/Not Ready - why]
- Startups: [Ready/Not Ready - why]

### Your Competitive Position:
[Honest assessment of where they stand in the job market]

### Salary Expectations (Realistic):
[Based on their actual experience level]
        """
        
        return await self.think(prompt, {})
    
    
    async def _create_personalized_learning_plan(
        self,
        resume_text: str,
        target_role: str,
        timeframe: str,
        timeframe_months: int
    ) -> str:
        """Create a learning plan based on resume gaps."""
        
        prompt = f"""
Based on this resume, create a PERSONALIZED learning plan for {target_role} in {timeframe}.

RESUME:
---
{resume_text}
---

Analyze what they already know (from their resume) and what they need to learn.

## 📚 Personalized Learning Plan

### What You Already Know (from your resume):
[List skills/experience they already have - don't make them relearn these]

### What You Need to Learn (Gaps):
[Based on their resume, what's missing for {target_role}?]

### Priority Learning Path:

#### Phase 1: Critical Gaps (First {timeframe_months // 3 or 1} months)
[Most important skills they're missing]
- Skill 1: [Why it's critical] - Resources: [Specific courses/books]
- Skill 2: ...

#### Phase 2: Experience Building (Next {timeframe_months // 3 or 1} months)
[Projects they need to build - based on what's MISSING from their resume]
- Project 1: [Description] - This fills the gap of: [What gap]
- Project 2: ...

#### Phase 3: Polish & Apply (Final stretch)
[Interview prep, portfolio, applications]

### Projects You MUST Build:
[Specific to their gaps - not generic projects]
1. [Project name]: [Description] - This proves you can [skill]
2. [Project name]: [Description]
3. [Project name]: [Description]

### Weekly Time Commitment:
[Realistic hours based on how much they need to learn]

### Realistic Timeline:
[Is {timeframe} enough? If not, what's realistic?]
        """
        
        return await self.think(prompt, {})
    
    
    async def _create_application_readiness(
        self,
        resume_text: str,
        target_role: str,
        timeframe: str
    ) -> str:
        """Assess application readiness based on resume."""
        
        prompt = f"""
Based on this resume, assess if they're ready to apply for {target_role} positions.

RESUME:
---
{resume_text}
---

## 📝 Application Readiness Assessment

### Should You Apply NOW?
[Yes/No/Maybe - with explanation based on their resume]

### Resume Strengths (Keep These):
[What's good in their resume that they should highlight]

### Resume Weaknesses (Fix These):
[What's weak or missing]

### Resume Improvement Suggestions:
[Specific changes to their resume]
1. [Suggestion 1]
2. [Suggestion 2]
3. [Suggestion 3]

### Interview Readiness:
Based on your resume, here's what interviewers will likely ask:
- [Topic 1]: Are you ready? [Yes/No/Needs work]
- [Topic 2]: Are you ready? [Yes/No/Needs work]
- [Topic 3]: Are you ready? [Yes/No/Needs work]

### Questions You'll Struggle With:
[Based on gaps in their resume]
1. [Question] - Why you'll struggle: [Reason]
2. [Question] - Why you'll struggle: [Reason]

### When to Start Applying:
[Based on their current state]
- Apply now to: [Types of companies]
- Wait X months for: [Types of companies]
- Need X more experience for: [Types of companies]

### Your Callback Rate Prediction:
[Based on their resume quality]
- Current state: ~X% callback rate
- After improvements: ~X% callback rate

### Action Plan:
[Prioritized list]
1. [First priority]
2. [Second priority]
3. [Third priority]
        """
        
        return await self.think(prompt, {})
    
    
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
        """Fallback: Create reality check based on skills only (no resume)."""
        
        prompt = f"""
Give a REALITY CHECK for someone targeting {target_role} in {timeframe}.

NOTE: No resume was provided, so this is based on skills only.

THEIR SKILLS: {', '.join(current_skills) if current_skills else 'None specified'}
REQUIRED FOR {target_role}: {', '.join(required_skills)}
SKILLS THEY HAVE: {', '.join(matched_skills) if matched_skills else 'None'}
SKILLS MISSING: {', '.join(skill_gaps) if skill_gaps else 'None'}
READINESS: {readiness_score}%

## 🚨 REALITY CHECK (Skills-Based)

### ⚠️ Limited Analysis
No resume was uploaded, so this analysis is based only on the skills you selected.
**For a complete analysis, please upload your resume.**

### Your Readiness: {readiness_score}%
[Explain what this means]

### ✅ Skills You Have ({len(matched_skills)}/{len(required_skills)}):
{chr(10).join(f'- {s}' for s in matched_skills) if matched_skills else '- None of the required skills'}

### ❌ Skills You're Missing ({len(skill_gaps)}/{len(required_skills)}):
{chr(10).join(f'- {s}' for s in skill_gaps) if skill_gaps else '- None! You have all required skills.'}

### ⏰ Is {timeframe} Realistic?
[Based on skill gaps]

### 📋 What You Need to Do:
[Specific actions for each missing skill]

### 💡 Bottom Line:
[Honest assessment]

**TIP: Upload your resume for a much more detailed and personalized analysis!**
        """
        
        return await self.think(prompt, {})