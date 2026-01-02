"""
Job Scraper Plugin - Native Function

This plugin fetches real job postings from free APIs.
It's a "native function" because it's written in Python code,
not using AI/LLM.
"""

import aiohttp
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from semantic_kernel.functions import kernel_function


class JobScraperPlugin:
    """
    A plugin that scrapes job postings from multiple free APIs.
    
    What's a Plugin?
    - A collection of related functions
    - Can be added to the kernel
    - Functions can be called by AI planners or manually
    """
    
    def __init__(self):
        """
        Constructor - runs when you create a new JobScraperPlugin instance
        """
        # Base URLs for free job APIs
        self.remotive_url = "https://remotive.com/api/remote-jobs"
        self.arbeitnow_url = "https://www.arbeitnow.com/api/job-board-api"
        
        print("🔧 JobScraperPlugin initialized")
    
    
    @kernel_function(
        name="scrape_genai_jobs",
        description="Fetches recent GenAI and ML engineering job postings from multiple sources"
    )
    async def scrape_genai_jobs(
        self, 
        keywords: str = "AI,machine learning,GenAI,LLM",
        limit: int = 20
    ) -> str:
        """
        Scrapes job boards for GenAI-related positions.
        
        Args:
            keywords: Comma-separated keywords to search for
            limit: Maximum number of jobs to return
        
        Returns:
            JSON string containing job listings
        
        The @kernel_function decorator tells Semantic Kernel:
        - This function can be called by the kernel
        - AI planners can use this function
        - It has a name and description for the AI to understand
        """
        
        print(f"🔍 Searching for jobs with keywords: {keywords}")
        print(f"📊 Limit: {limit} jobs")
        
        all_jobs = []
        
        # Fetch from multiple sources
        try:
            # Source 1: Remotive (Remote jobs)
            remotive_jobs = await self._fetch_remotive_jobs(keywords)
            all_jobs.extend(remotive_jobs)
            print(f"✅ Found {len(remotive_jobs)} jobs from Remotive")
            
            # Source 2: Arbeitnow (International jobs)
            arbeitnow_jobs = await self._fetch_arbeitnow_jobs(keywords)
            all_jobs.extend(arbeitnow_jobs)
            print(f"✅ Found {len(arbeitnow_jobs)} jobs from Arbeitnow")
            
        except Exception as e:
            print(f"❌ Error fetching jobs: {e}")
            return json.dumps({"error": str(e), "jobs": []})
        
        # Limit results
        all_jobs = all_jobs[:limit]
        
        # Format response
        result = {
            "total_jobs": len(all_jobs),
            "timestamp": datetime.now().isoformat(),
            "keywords_searched": keywords,
            "jobs": all_jobs
        }
        
        print(f"🎉 Total jobs found: {len(all_jobs)}")
        
        # Return as JSON string (Semantic Kernel functions return strings)
        return json.dumps(result, indent=2)
    
    
    async def _fetch_remotive_jobs(self, keywords: str) -> List[Dict]:
        """
        Private helper method to fetch from Remotive API.
        
        The underscore _ prefix means this is a "private" method
        (not meant to be called from outside this class)
        """
        jobs = []
        
        try:
            # Create async HTTP session
            async with aiohttp.ClientSession() as session:
                # Make GET request
                async with session.get(self.remotive_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Filter jobs by keywords
                        keyword_list = [k.strip().lower() for k in keywords.split(",")]
                        
                        for job in data.get("jobs", [])[:50]:  # Check first 50
                            title = job.get("title", "").lower()
                            description = job.get("description", "").lower()
                            
                            # Check if any keyword matches
                            if any(kw in title or kw in description for kw in keyword_list):
                                jobs.append({
                                    "title": job.get("title"),
                                    "company": job.get("company_name"),
                                    "location": "Remote",
                                    "url": job.get("url"),
                                    "posted_date": job.get("publication_date"),
                                    "source": "Remotive"
                                })
        
        except Exception as e:
            print(f"⚠️ Remotive API error: {e}")
        
        return jobs
    
    
    async def _fetch_arbeitnow_jobs(self, keywords: str) -> List[Dict]:
        """
        Private helper method to fetch from Arbeitnow API.
        """
        jobs = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.arbeitnow_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        keyword_list = [k.strip().lower() for k in keywords.split(",")]
                        
                        for job in data.get("data", [])[:50]:
                            title = job.get("title", "").lower()
                            description = job.get("description", "").lower()
                            
                            if any(kw in title or kw in description for kw in keyword_list):
                                jobs.append({
                                    "title": job.get("title"),
                                    "company": job.get("company_name"),
                                    "location": job.get("location", "N/A"),
                                    "url": job.get("url"),
                                    "posted_date": job.get("created_at"),
                                    "source": "Arbeitnow"
                                })
        
        except Exception as e:
            print(f"⚠️ Arbeitnow API error: {e}")
        
        return jobs
    
    
    @kernel_function(
        name="get_job_stats",
        description="Analyzes scraped jobs and returns statistics"
    )
    async def get_job_stats(self, jobs_json: str) -> str:
        """
        Another native function that analyzes job data.
        
        This shows how plugins can have multiple functions!
        """
        try:
            data = json.loads(jobs_json)
            jobs = data.get("jobs", [])
            
            # Calculate stats
            total = len(jobs)
            companies = set(job.get("company") for job in jobs)
            sources = {}
            
            for job in jobs:
                source = job.get("source", "Unknown")
                sources[source] = sources.get(source, 0) + 1
            
            stats = {
                "total_jobs": total,
                "unique_companies": len(companies),
                "jobs_by_source": sources,
                "top_companies": list(companies)[:10]
            }
            
            return json.dumps(stats, indent=2)
        
        except Exception as e:
            return json.dumps({"error": str(e)})