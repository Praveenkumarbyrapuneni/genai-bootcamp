# api/main.py

"""
FastAPI Backend for CareerPath AI
Connects the Next.js frontend with the Python AI agents.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import only what we need - removed Semantic Kernel imports
from src.database.cosmos_manager import CareerDataManager
from src.database.supabase_tracker import get_tracker

app = FastAPI(
    title="CareerPath AI API",
    description="AI-powered career analysis API",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    user_id: str
    user_email: Optional[str] = None  # Added for tracking
    target_role: str
    current_skills: list[str]
    timeframe_months: int = 6
    timeframe_display: Optional[str] = None  # e.g., "1 day", "6 months", "2 years"
    resume_text: Optional[str] = None
    
    @field_validator('target_role')
    @classmethod
    def validate_target_role(cls, v: str) -> str:
        """Validate that target_role is not empty."""
        v = v.strip()
        if not v:
            raise ValueError("Please enter a message or career goal")
        
        return v


class BulkDeleteRequest(BaseModel):
    ids: list[str]
    user_id: str


class BulkArchiveRequest(BaseModel):
    ids: list[str]
    user_id: str
    is_archived: bool


class AnalysisResponse(BaseModel):
    final_recommendations: str
    market_research: str
    learning_plan: str
    application_strategy: str


@app.get("/")
async def root():
    return {"message": "CareerPath AI API is running 🚀"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_career(request: AnalysisRequest):
    """
    Run comprehensive career analysis using AI agents.
    """
    try:
        # Quick validation
        if not request.target_role or len(request.target_role.strip()) < 1:
            raise HTTPException(
                status_code=400, 
                detail="Please enter a message or career goal"
            )
        
        # For simple conversational inputs, return a quick response without AI
        simple_inputs = ['hello', 'hi', 'hey', 'test', 'testing']
        if request.target_role.lower().strip() in simple_inputs:
            return AnalysisResponse(
                final_recommendations=f"Hello! 👋 I'm CareerPath AI, your career advisor.\n\nI can help you with:\n- Career path analysis\n- Skills gap assessment\n- Learning roadmaps\n- Job market insights\n\nTo get started, tell me about your target role (e.g., 'Data Analyst', 'Software Engineer') and your current skills!",
                market_research="I'm ready to analyze market trends for any role you're interested in.",
                learning_plan="Share your target role and current skills to get a personalized learning plan.",
                application_strategy="Let me know your career goals and I'll help you create an application strategy."
            )
        
        # Use Groq directly for fast responses
        from src.groq_client import get_groq_client
        groq = get_groq_client()
        
        # Build the analysis prompt
        resume_info = f"\n\nRESUME:\n{request.resume_text[:2000]}" if request.resume_text else ""
        skills_info = f"\n\nCURRENT SKILLS: {', '.join(request.current_skills)}" if request.current_skills else ""
        
        prompt = f"""You are a brutally honest career advisor. Analyze this person's career goals.

TARGET ROLE: {request.target_role}
TIMEFRAME: {request.timeframe_display or f'{request.timeframe_months} months'}{skills_info}{resume_info}

Provide a detailed analysis with:
1. Reality Check - honest assessment of readiness (0-100%)
2. Strengths and weaknesses
3. What they need to learn
4. Timeline feasibility
5. Specific action items

Be direct and honest."""

        # Get AI response
        final_recommendations = await groq.get_completion(
            prompt=prompt,
            system_prompt="You are a brutally honest career advisor. Give reality checks, not motivational speeches.",
            max_tokens=2000
        )
        
        # Generate other sections
        market_prompt = f"Analyze the job market for {request.target_role}. Include: demand, salary range, required skills, and company types hiring."
        market_research = await groq.get_completion(market_prompt, max_tokens=1500)
        
        learning_prompt = f"Create a {request.timeframe_display or f'{request.timeframe_months} month'} learning plan for becoming a {request.target_role}."
        learning_plan = await groq.get_completion(learning_prompt, max_tokens=1500)
        
        strategy_prompt = f"What's the application strategy for {request.target_role}? When to apply, where to apply, resume tips."
        application_strategy = await groq.get_completion(strategy_prompt, max_tokens=1500)
        
        results = {
            "final_recommendations": final_recommendations,
            "market_research": market_research,
            "learning_plan": learning_plan,
            "application_strategy": application_strategy
        }
        
        # Log the search to Supabase
        try:
            tracker = get_tracker()
            tracker.log_search(
                user_id=request.user_id,
                user_email=request.user_email,
                target_role=request.target_role,
                current_skills=request.current_skills,
                timeframe=request.timeframe_display or f"{request.timeframe_months} months",
                resume_uploaded=bool(request.resume_text)
            )
        except Exception as track_error:
            print(f"Tracking error (non-critical): {track_error}")
        
        # Save to database
        try:
            db_manager = CareerDataManager()
            db_manager.save_career_analysis(
                user_id=request.user_id,
                role=request.target_role,
                analysis_data=results
            )
        except Exception as db_error:
            print(f"Database save error (non-critical): {db_error}")
        
        return AnalysisResponse(
            final_recommendations=results.get("final_recommendations", "No recommendations available."),
            market_research=results.get("market_research", "No market data available."),
            learning_plan=results.get("learning_plan", "No learning plan available."),
            application_strategy=results.get("application_strategy", "No strategy available.")
        )
        
    except ValueError as ve:
        # Validation error from Pydantic - return 400 Bad Request
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse uploaded resume and extract text.
    """
    try:
        content = await file.read()
        
        # Handle different file types
        filename = (file.filename or "unknown.txt").lower()
        
        if filename.endswith('.txt'):
            text = content.decode('utf-8')
        elif filename.endswith('.pdf'):
            # Try to extract text from PDF
            try:
                import PyPDF2  # type: ignore
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            except ImportError:
                text = "[PDF parsing requires PyPDF2. Please upload a .txt file or paste your resume text.]"
        elif filename.endswith('.docx'):
            try:
                import docx  # type: ignore
                import io
                doc = docx.Document(io.BytesIO(content))
                text = "\n".join([para.text for para in doc.paragraphs])
            except ImportError:
                text = "[DOCX parsing requires python-docx. Please upload a .txt file or paste your resume text.]"
        else:
            text = content.decode('utf-8', errors='ignore')
        
        # Extract skills from resume text
        extracted_skills = extract_skills_from_resume(text)
        
        return {
            "text": text, 
            "filename": file.filename,
            "extracted_skills": extracted_skills
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")


def extract_skills_from_resume(text: str) -> list[str]:
    """
    Extract skills from resume text using keyword matching.
    """
    # Common skills to look for
    all_skills = [
        # Programming Languages
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",
        # Web Development
        "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring", "HTML", "CSS", "REST API", "GraphQL",
        # Data & ML
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Keras",
        "Data Analysis", "Data Science", "Data Visualization", "Tableau", "Power BI", "Excel", "Statistics",
        "NLP", "Computer Vision", "Neural Networks",
        # AI/LLM
        "LLM", "LLMs", "Large Language Models", "GPT", "OpenAI", "Azure OpenAI", "Prompt Engineering", 
        "RAG", "Retrieval Augmented Generation", "Vector Databases", "LangChain", "Semantic Kernel", "Fine-tuning",
        "Hugging Face", "Transformers",
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions",
        "Terraform", "Ansible", "Linux", "DevOps", "MLOps",
        # Other
        "Git", "Agile", "Scrum", "System Design", "Microservices", "API Development",
        "ETL", "Data Cleaning", "A/B Testing", "Business Intelligence", "Reporting",
        "Data Structures", "Algorithms", "Problem Solving",
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in all_skills:
        # Check if skill exists in text (case insensitive)
        if skill.lower() in text_lower:
            # Avoid duplicates
            if skill not in found_skills:
                found_skills.append(skill)
    
    return found_skills


@app.get("/api/history/{user_id}")
async def get_history(user_id: str, include_archived: bool = False):
    """
    Get analysis history for a user.
    Filters out deleted records by default.
    Optionally includes archived records.
    """
    try:
        db_manager = CareerDataManager()
        history = db_manager.get_user_history(user_id, include_archived=include_archived)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/history/bulk-delete")
async def bulk_delete_history(request: BulkDeleteRequest):
    """
    Soft delete multiple analysis records.
    Verifies ownership before deleting.
    
    Security: Validates that all records belong to the requesting user.
    """
    try:
        if not request.ids:
            raise HTTPException(status_code=400, detail="No IDs provided")
        
        if len(request.ids) > 100:
            raise HTTPException(status_code=400, detail="Cannot delete more than 100 items at once")
        
        db_manager = CareerDataManager()
        result = db_manager.bulk_delete(request.ids, request.user_id)
        
        return {
            "success": True,
            "updated": result["updated"],
            "failed": result["failed"],
            "failed_ids": result["failed_ids"],
            "message": f"Deleted {result['updated']} item(s)" + 
                      (f", {result['failed']} failed" if result['failed'] > 0 else "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Bulk delete error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/history/bulk-archive")
async def bulk_archive_history(request: BulkArchiveRequest):
    """
    Archive or unarchive multiple analysis records.
    Verifies ownership before updating.
    
    Security: Validates that all records belong to the requesting user.
    """
    try:
        if not request.ids:
            raise HTTPException(status_code=400, detail="No IDs provided")
        
        if len(request.ids) > 100:
            raise HTTPException(status_code=400, detail="Cannot archive more than 100 items at once")
        
        db_manager = CareerDataManager()
        result = db_manager.bulk_archive(request.ids, request.user_id, request.is_archived)
        
        action = "archived" if request.is_archived else "unarchived"
        
        return {
            "success": True,
            "updated": result["updated"],
            "failed": result["failed"],
            "failed_ids": result["failed_ids"],
            "message": f"{action.capitalize()} {result['updated']} item(s)" + 
                      (f", {result['failed']} failed" if result['failed'] > 0 else "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Bulk archive error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/searches")
async def get_all_searches(limit: int = 100):
    """Get all user searches (admin endpoint)."""
    try:
        tracker = get_tracker()
        searches = tracker.get_all_searches(limit)
        return {"searches": searches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/popular-roles")
async def get_popular_roles(limit: int = 10):
    """Get most popular searched roles."""
    try:
        tracker = get_tracker()
        roles = tracker.get_popular_roles(limit)
        return {"popular_roles": roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/summary")
async def get_analytics_summary():
    """Get analytics summary."""
    try:
        tracker = get_tracker()
        summary = tracker.get_analytics_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/user/{user_id}/searches")
async def get_user_searches(user_id: str, limit: int = 50):
    """Get search history for a specific user."""
    try:
        tracker = get_tracker()
        searches = tracker.get_user_searches(user_id, limit)
        return {"searches": searches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
