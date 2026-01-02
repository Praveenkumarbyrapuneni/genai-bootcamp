import logging
from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

class CareerPlanner:
    """
    A specialized planner for career development tasks.
    
    Instead of a generic "do anything" planner, this is a 
    "Domain Specific Planner" tuned for career coaching.
    """

    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.logger = logging.getLogger(__name__)

    async def execute_custom_plan(self, goal: str) -> str:
        """
        Executes a general goal by asking the AI to form a plan and execute it.
        """
        prompt = """
        You are an expert Career Strategist and Planner.
        
        GOAL: {{$goal}}
        
        Please:
        1. Break this goal down into logical steps.
        2. Execute the necessary reasoning.
        3. Provide a clear, actionable summary.
        """
        
        print(f"   🤖 Planner thinking about: {goal[:50]}...")
        
        # Invoke the prompt using the kernel
        result = await self.kernel.invoke_prompt(
            prompt=prompt,
            arguments=KernelArguments(goal=goal)
        )
        return str(result)

    async def create_job_preparation_plan(
        self, 
        job_title: str, 
        company: str, 
        your_current_skills: list
    ) -> str:
        """
        Creates a specific step-by-step plan to prepare for a job application.
        """
        skills_str = ", ".join(your_current_skills)
        
        prompt = """
        You are a Hiring Manager creating a preparation plan for a candidate.
        
        TARGET ROLE: {{$job_title}} at {{$company}}
        CANDIDATE SKILLS: {{$skills_str}}
        
        Create a detailed preparation plan that includes:
        1. Skill Gap Analysis (What are they missing?)
        2. Project Ideas (What should they build to prove they can do the job?)
        3. Resume Tweaks (What keywords must be emphasized?)
        4. Interview Prep (Top 3 questions to expect)
        
        Format it as a professional report.
        """
        
        print(f"   🤖 Planner analyzing role: {job_title}...")
        
        result = await self.kernel.invoke_prompt(
            prompt=prompt,
            arguments=KernelArguments(
                job_title=job_title, 
                company=company, 
                skills_str=skills_str
            )
        )
        return str(result)

    async def create_learning_roadmap(
        self, 
        target_role: str, 
        timeframe_weeks: int, 
        current_level: str
    ) -> str:
        """
        Generates a week-by-week learning schedule.
        """
        prompt = """
        Create a structured Learning Roadmap.
        
        ROLE: {{$target_role}}
        TIMEFRAME: {{$timeframe_weeks}} weeks
        CURRENT LEVEL: {{$current_level}}
        
        Structure this as a Week-by-Week plan.
        For each phase, specify:
        - Topic
        - Key Concepts to Master
        - A small hands-on exercise
        
        Ensure the progression is logical (Foundation -> Advanced -> Mastery).
        """
        
        print(f"   🤖 Planner building {timeframe_weeks}-week roadmap...")
        
        result = await self.kernel.invoke_prompt(
            prompt=prompt,
            arguments=KernelArguments(
                target_role=target_role,
                timeframe_weeks=timeframe_weeks,
                current_level=current_level
            )
        )
        return str(result)

    async def analyze_job_market_trends(self, role_type: str, location: str) -> str:
        """
        Analyzes market trends for a specific role.
        """
        prompt = """
        Act as a Labor Market Analyst.
        
        Analyze the current trends for:
        ROLE: {{$role_type}}
        LOCATION: {{$location}}
        
        Provide insights on:
        1. Demand (Is it growing?)
        2. Salary Expectations (Range)
        3. Top 3 Trending Technologies in this space right now
        4. "Hidden Gems" (Industries hiring for this that people forget)
        """
        
        print(f"   🤖 Planner analyzing market for: {role_type}...")
        
        result = await self.kernel.invoke_prompt(
            prompt=prompt,
            arguments=KernelArguments(role_type=role_type, location=location)
        )
        return str(result)

    async def create_application_strategy(
        self, 
        job_description: str, 
        your_background: str
    ) -> str:
        """
        Develops a strategy to apply for a specific job description.
        """
        prompt = """
        You are a Career Coach helping a user apply for a specific job.
        
        JOB DESCRIPTION:
        {{$job_description}}
        
        USER BACKGROUND:
        {{$your_background}}
        
        Devise a winning Application Strategy:
        1. The "Hook": What is the single strongest match point to open the cover letter with?
        2. The "Gap": Identify one weakness and how to address it proactively.
        3. The "Portfolio": Suggest one specific artifact/demo to send with the application.
        """
        
        print("   🤖 Planner devising application strategy...")
        
        result = await self.kernel.invoke_prompt(
            prompt=prompt,
            arguments=KernelArguments(
                job_description=job_description, 
                your_background=your_background
            )
        )
        return str(result)