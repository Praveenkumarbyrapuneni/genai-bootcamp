# api/main.py

"""
FastAPI Backend for CareerPath AI
Connects the Next.js frontend with the Python AI agents.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.kernel_config import create_kernel
from src.agents.career_advisor import CareerAdvisorAgent
from src.database.cosmos_manager import CareerDataManager

app = FastAPI(
    title="CareerPath AI API",
    description="AI-powered career analysis API",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    user_id: str
    target_role: str
    current_skills: list[str]
    timeframe_months: int = 6


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
        # Initialize the AI system
        kernel = create_kernel()
        advisor = CareerAdvisorAgent(kernel)
        
        # Run analysis
        results = await advisor.comprehensive_career_analysis(
            target_role=request.target_role,
            current_skills=request.current_skills,
            timeframe_months=request.timeframe_months
        )
        
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/{user_id}")
async def get_history(user_id: str):
    """
    Get analysis history for a user.
    """
    try:
        db_manager = CareerDataManager()
        history = db_manager.get_user_history(user_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
