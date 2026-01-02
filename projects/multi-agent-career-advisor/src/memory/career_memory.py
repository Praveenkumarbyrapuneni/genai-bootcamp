# src/memory/career_memory.py

"""
Career Memory Manager

This module manages memory for our AI agent:
- Stores skills and their proficiency levels
- Remembers job analyses
- Tracks progress over time
- Enables semantic search (find similar skills)

Uses vector embeddings to understand similarity!
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from semantic_kernel import Kernel
from semantic_kernel.memory import SemanticTextMemory, VolatileMemoryStore
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CareerMemory:
    """
    Manages all memory operations for the career AI agent.
    """
    
    def __init__(self, kernel: Kernel):
        """
        Initialize memory system.
        """
        self.kernel = kernel
        
        # --- SAFE KEY LOADING ---
        # We read keys directly from environment variables
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        deployment_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

        if not deployment_name:
            print("⚠️ WARNING: AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME not found in .env")
            print("   Using default 'text-embedding-ada-002'")
            deployment_name = "text-embedding-ada-002"

        # Create embedding service
        self.embedding_service = AzureTextEmbedding(
            service_id="embedding_service",
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version="2023-05-15" # Standard stable version for embeddings
        )
        
        # Create memory store (in-memory for now)
        memory_store = VolatileMemoryStore()
        
        # Create semantic memory
        self.memory = SemanticTextMemory(
            storage=memory_store,
            embeddings_generator=self.embedding_service
        )
        
        # Collection names
        self.SKILLS_COLLECTION = "my_skills"
        self.JOBS_COLLECTION = "analyzed_jobs"
        self.PROGRESS_COLLECTION = "learning_progress"
        
        print("🧠 CareerMemory initialized")
        print("📦 Using VolatileMemoryStore (in-memory)")
        print(f"✨ Embedding service connected: {deployment_name}")
    
    
    async def store_skill(
        self, 
        skill_name: str, 
        proficiency: str, 
        evidence: str,
        category: str = "technical"
    ) -> None:
        """Store a skill in memory with context."""
        text = f"""
        Skill: {skill_name}
        Proficiency: {proficiency}
        Category: {category}
        Evidence: {evidence}
        """
        
        await self.memory.save_information(
            collection=self.SKILLS_COLLECTION,
            id=f"skill_{skill_name.lower().replace(' ', '_')}",
            text=text.strip()
        )
        print(f"✅ Stored skill: {skill_name} ({proficiency})")
    
    
    async def get_skill(self, skill_name: str) -> Optional[Dict]:
        """Retrieve a specific skill from memory."""
        try:
            results = await self.memory.search(
                collection=self.SKILLS_COLLECTION,
                query=skill_name,
                limit=1
            )
            if results:
                result = results[0]
                return {
                    "skill": skill_name,
                    "text": result.text,
                    "relevance": result.relevance
                }
            return None
        except Exception as e:
            print(f"⚠️ Error retrieving skill: {e}")
            return None
    
    
    async def find_similar_skills(
        self, 
        query: str, 
        limit: int = 5,
        min_relevance: float = 0.7
    ) -> List[Dict]:
        """Find skills similar to a query using semantic search."""
        print(f"🔍 Searching for skills similar to: '{query}'")
        try:
            results = await self.memory.search(
                collection=self.SKILLS_COLLECTION,
                query=query,
                limit=limit,
                min_relevance_score=min_relevance
            )
            similar_skills = []
            for result in results:
                similar_skills.append({
                    "text": result.text,
                    "relevance": result.relevance,
                    "id": result.id
                })
                print(f"  📌 {result.id} (relevance: {result.relevance:.2f})")
            return similar_skills
        except Exception as e:
            print(f"❌ Error in similarity search: {e}")
            return []


    async def store_job_analysis(
        self,
        job_title: str,
        company: str,
        analysis_result: Dict,
        match_percentage: float
    ) -> None:
        """Store an analyzed job in memory."""
        text = f"""
        Job: {job_title}
        Company: {company}
        Match: {match_percentage}%
        Required Skills: {', '.join(analysis_result.get('required_skills', []))}
        """
        
        job_id = f"job_{company.lower().replace(' ', '_')}_{job_title.lower().replace(' ', '_')}"
        
        await self.memory.save_information(
            collection=self.JOBS_COLLECTION,
            id=job_id,
            text=text.strip()
        )
        print(f"💼 Stored job analysis: {job_title} at {company}")
    
    
    async def find_similar_jobs(self, query: str, limit: int = 5) -> List[Dict]:
        """Find jobs similar to a query."""
        print(f"🔍 Finding jobs similar to: '{query}'")
        try:
            results = await self.memory.search(
                collection=self.JOBS_COLLECTION,
                query=query,
                limit=limit
            )
            jobs = []
            for result in results:
                jobs.append({
                    "text": result.text,
                    "relevance": result.relevance,
                    "id": result.id
                })
            return jobs
        except Exception as e:
            print(f"❌ Error searching jobs: {e}")
            return []


    async def store_learning_progress(
        self,
        skill: str,
        progress_percentage: int,
        notes: str
    ) -> None:
        """
        Track learning progress for a skill.
        """
        text = f"""
        Learning: {skill}
        Progress: {progress_percentage}%
        Notes: {notes}
        Updated: {datetime.now().isoformat()}
        """
        
        progress_id = f"progress_{skill.lower().replace(' ', '_')}"
        
        await self.memory.save_information(
            collection=self.PROGRESS_COLLECTION,
            id=progress_id,
            text=text.strip()
        )
        print(f"📈 Updated progress: {skill} → {progress_percentage}%")


    async def get_all_skills(self) -> List[str]:
        """
        Get list of all skills in memory.
        Note: VolatileMemoryStore doesn't support easy listing, but this prevents errors.
        """
        print("ℹ️ Listing all skills not supported in VolatileMemoryStore")
        return []


    async def calculate_skill_coverage(
        self,
        required_skills: List[str]
    ) -> Tuple[int, List[str], List[str]]:
        """
        Calculate what percentage of required skills you have.
        """
        matched = []
        missing = []
        
        for skill in required_skills:
            # Search if we have this skill in memory
            similar = await self.find_similar_skills(
                query=skill,
                limit=1,
                min_relevance=0.75 # High threshold for "having" the skill
            )
            
            if similar:
                matched.append(skill)
                print(f"  ✅ Have: {skill} (Matched: {similar[0]['text'][:30]}...)")
            else:
                missing.append(skill)
                print(f"  ❌ Missing: {skill}")
        
        percentage = int((len(matched) / len(required_skills)) * 100) if required_skills else 0
        
        return percentage, matched, missing