# src/plugins/job_intelligence/analyzer.py

"""
Skills Analyzer Plugin - Semantic Functions

This plugin uses AI to analyze job descriptions.
Unlike native functions, these use LLM to understand and reason.
"""

import json
import os
from typing import Dict, Optional
from semantic_kernel.functions import kernel_function
from semantic_kernel import Kernel
from semantic_kernel.prompt_template import PromptTemplateConfig


class SkillsAnalyzerPlugin:
    """
    A plugin that uses semantic functions (AI-powered prompts)
    to analyze job descriptions and extract structured information.
    """
    
    def __init__(self, kernel: Kernel):
        """
        Constructor - needs a kernel to make AI calls
        
        Args:
            kernel: The Semantic Kernel instance (with AI service)
        """
        self.kernel = kernel
        
        # Path to our prompt templates
        self.prompts_dir = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', '..', 
            'prompts', 
            'skills_analyzer'
        )
        
        print("🧠 SkillsAnalyzerPlugin initialized")
    
    
    def _load_prompt_template(self, filename: str) -> str:
        """
        Helper method to load prompt from file
        
        Args:
            filename: Name of the prompt file (e.g., 'extract_skills.txt')
        
        Returns:
            The prompt template as a string
        """
        prompt_path = os.path.join(self.prompts_dir, filename)
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Prompt template not found: {prompt_path}\n"
                f"Make sure you created the file in: prompts/skills_analyzer/"
            )
    
    
    @kernel_function(
        name="extract_skills_from_job",
        description="Uses AI to extract technical skills, experience level, and requirements from a job description"
    )
    async def extract_skills_from_job(self, job_description: str) -> str:
        """
        Semantic function that analyzes a job description using AI.
        
        This is different from native functions because:
        1. It uses an LLM (AI) to understand the text
        2. It can reason about context and meaning
        3. It costs tokens (money) to run
        4. Results can vary slightly each time
        
        Args:
            job_description: The full text of a job posting
        
        Returns:
            JSON string with extracted skills and requirements
        """
        
        print(f"🔍 Analyzing job description with AI...")
        print(f"📝 Job description length: {len(job_description)} characters")
        
        # Load our prompt template
        prompt_template = self._load_prompt_template("extract_skills.txt")
        
        # Create the prompt configuration
        # This tells SK how to use this prompt
        prompt_config = PromptTemplateConfig(
            template=prompt_template,
            name="extract_skills",
            description="Extracts skills from job description",
            input_variables=[
                {"name": "input", "description": "The job description text"}
            ]
        )
        
        try:
            # Invoke the AI with our prompt and the job description
            # The {{$input}} in the prompt gets replaced with job_description
            result = await self.kernel.invoke_prompt(
                prompt=prompt_template,
                function_name="extract_skills",
                arguments={"input": job_description}
            )
            
            # The AI returns text, let's try to parse it as JSON
            result_text = str(result).strip()
            
            # Sometimes AI adds markdown code blocks, remove them
            if result_text.startswith("```json"):
                result_text = result_text[7:]  # Remove ```json
            if result_text.startswith("```"):
                result_text = result_text[3:]  # Remove ```
            if result_text.endswith("```"):
                result_text = result_text[:-3]  # Remove trailing ```
            
            result_text = result_text.strip()
            
            # Validate it's valid JSON
            parsed = json.loads(result_text)
            
            print(f"✅ Successfully extracted {len(parsed.get('required_skills', []))} required skills")
            print(f"✅ Experience level: {parsed.get('experience_level', 'unknown')}")
            
            return json.dumps(parsed, indent=2)
            
        except json.JSONDecodeError as e:
            print(f"⚠️ AI returned invalid JSON: {e}")
            print(f"Raw response: {result_text[:200]}...")
            
            # Return error as JSON
            return json.dumps({
                "error": "Failed to parse AI response",
                "raw_response": result_text[:500]
            })
        
        except Exception as e:
            print(f"❌ Error during AI analysis: {e}")
            return json.dumps({"error": str(e)})
    
    
    @kernel_function(
        name="compare_skills_to_profile",
        description="Compares job requirements to a candidate's skills and calculates match percentage"
    )
    async def compare_skills_to_profile(
        self, 
        job_skills_json: str, 
        candidate_skills: str
    ) -> str:
        """
        Another semantic function that does comparison using AI reasoning.
        
        This shows how semantic functions can do complex reasoning
        that would be hard to program with if/else logic.
        
        Args:
            job_skills_json: JSON from extract_skills_from_job
            candidate_skills: Comma-separated list of candidate's skills
        
        Returns:
            JSON with match analysis
        """
        
        print(f"🎯 Comparing candidate skills to job requirements...")
        
        # Create a prompt for comparison
        comparison_prompt = f"""
You are a career advisor. Compare a candidate's skills to a job's requirements.

Job Requirements:
{job_skills_json}

Candidate's Skills:
{candidate_skills}

Analyze the match and return ONLY a valid JSON object:
{{
  "match_percentage": 75,
  "matched_skills": ["skill1", "skill2"],
  "missing_critical_skills": ["skill3"],
  "transferable_skills": ["skill4"],
  "recommendation": "Good match but needs to learn X",
  "readiness_level": "ready|almost_ready|needs_development"
}}

Consider:
- Direct skill matches
- Transferable/related skills
- Experience level fit
- Critical vs nice-to-have skills
"""
        
        try:
            result = await self.kernel.invoke_prompt(
                prompt=comparison_prompt,
                function_name="compare_skills"
            )
            
            result_text = str(result).strip()
            
            # Clean markdown formatting
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            result_text = result_text.strip()
            
            # Validate JSON
            parsed = json.loads(result_text)
            
            print(f"📊 Match percentage: {parsed.get('match_percentage', 0)}%")
            print(f"✅ Matched skills: {len(parsed.get('matched_skills', []))}")
            print(f"⚠️ Missing critical: {len(parsed.get('missing_critical_skills', []))}")
            
            return json.dumps(parsed, indent=2)
            
        except Exception as e:
            print(f"❌ Error in comparison: {e}")
            return json.dumps({"error": str(e)})
    
    
    @kernel_function(
        name="generate_learning_recommendations",
        description="Generates personalized learning recommendations based on skill gaps"
    )
    async def generate_learning_recommendations(
        self, 
        missing_skills: str,
        current_level: str = "intermediate"
    ) -> str:
        """
        Uses AI to suggest learning resources and projects.
        
        This demonstrates how semantic functions can be creative
        and generate helpful content.
        
        Args:
            missing_skills: Comma-separated list of skills to learn
            current_level: beginner|intermediate|advanced
        
        Returns:
            JSON with learning recommendations
        """
        
        print(f"📚 Generating learning plan for: {missing_skills}")
        
        learning_prompt = f"""
You are a technical mentor for GenAI engineers.

Student's current level: {current_level}
Skills they need to learn: {missing_skills}

Create a focused learning plan. Return ONLY valid JSON:
{{
  "priority_order": ["skill1", "skill2", "skill3"],
  "estimated_weeks": 12,
  "learning_path": [
    {{
      "skill": "skill_name",
      "why_important": "explanation",
      "resources": [
        {{"type": "course", "name": "Course Name", "url": "https://...", "duration": "4 weeks"}},
        {{"type": "tutorial", "name": "Tutorial Name", "url": "https://..."}}
      ],
      "practice_projects": ["project idea 1", "project idea 2"],
      "estimated_time": "3 weeks"
    }}
  ],
  "quick_wins": ["Easy skill to start with"],
  "success_metrics": "How to know you've learned it"
}}

Focus on:
- Free/affordable resources
- Practical, hands-on learning
- Projects that build portfolio
- Resources specific to GenAI/ML engineering
"""
        
        try:
            result = await self.kernel.invoke_prompt(
                prompt=learning_prompt,
                function_name="learning_recommendations"
            )
            
            result_text = str(result).strip()
            
            # Clean formatting
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            result_text = result_text.strip()
            parsed = json.loads(result_text)
            
            print(f"✅ Generated learning plan: {parsed.get('estimated_weeks', 0)} weeks")
            print(f"📚 Resources for {len(parsed.get('learning_path', []))} skills")
            
            return json.dumps(parsed, indent=2)
            
        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            return json.dumps({"error": str(e)})