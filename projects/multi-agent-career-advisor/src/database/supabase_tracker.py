# src/database/supabase_tracker.py

"""
Supabase Activity Tracker for CareerPath AI
Tracks user searches, logins, and activity for analytics.
"""

import os
from datetime import datetime
from typing import Optional, Any
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class SupabaseActivityTracker:
    """
    Tracks user activity in Supabase database.
    
    Tables required in Supabase:
    - user_searches: Tracks what users search for
    - user_activity: Tracks general user activity (logins, page views, etc.)
    """
    
    def __init__(self):
        """Initialize Supabase client."""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        self.client: Optional[Client] = None
        
        if self.url and self.key:
            self.client = create_client(self.url, self.key)
        else:
            print("Warning: Supabase not configured for activity tracking")
    
    def log_search(
        self,
        user_id: str,
        user_email: Optional[str],
        target_role: str,
        current_skills: list[str],
        timeframe: str,
        resume_uploaded: bool = False
    ) -> bool:
        """
        Log a user's career search/analysis request.
        
        Args:
            user_id: User's unique ID
            user_email: User's email address
            target_role: The job role they're targeting
            current_skills: List of their current skills
            timeframe: Timeframe for their career plan
            resume_uploaded: Whether they uploaded a resume
            
        Returns:
            True if logged successfully, False otherwise
        """
        if not self.client:
            return False
        
        try:
            data = {
                "user_id": user_id,
                "user_email": user_email,
                "target_role": target_role,
                "current_skills": current_skills,
                "timeframe": timeframe,
                "resume_uploaded": resume_uploaded,
                "searched_at": datetime.utcnow().isoformat()
            }
            
            self.client.table("user_searches").insert(data).execute()
            return True
        except Exception as e:
            print(f"Error logging search: {e}")
            return False
    
    def log_activity(
        self,
        user_id: str,
        user_email: Optional[str],
        activity_type: str,
        details: Optional[dict] = None
    ) -> bool:
        """
        Log general user activity.
        
        Args:
            user_id: User's unique ID
            user_email: User's email address
            activity_type: Type of activity (login, logout, page_view, etc.)
            details: Additional details about the activity
            
        Returns:
            True if logged successfully, False otherwise
        """
        if not self.client:
            return False
        
        try:
            data = {
                "user_id": user_id,
                "user_email": user_email,
                "activity_type": activity_type,
                "details": details or {},
                "activity_at": datetime.utcnow().isoformat()
            }
            
            self.client.table("user_activity").insert(data).execute()
            return True
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False
    
    def get_user_searches(self, user_id: str, limit: int = 50) -> list:
        """
        Get search history for a specific user.
        
        Args:
            user_id: User's unique ID
            limit: Maximum number of records to return
            
        Returns:
            List of search records
        """
        if not self.client:
            return []
        
        try:
            response = self.client.table("user_searches") \
                .select("*") \
                .eq("user_id", user_id) \
                .order("searched_at", desc=True) \
                .limit(limit) \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting user searches: {e}")
            return []
    
    def get_all_searches(self, limit: int = 100) -> list:
        """
        Get all searches (admin view).
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of all search records
        """
        if not self.client:
            return []
        
        try:
            response = self.client.table("user_searches") \
                .select("*") \
                .order("searched_at", desc=True) \
                .limit(limit) \
                .execute()
            return response.data
        except Exception as e:
            print(f"Error getting all searches: {e}")
            return []
    
    def get_popular_roles(self, limit: int = 10) -> list:
        """
        Get most searched roles.
        
        Args:
            limit: Maximum number of roles to return
            
        Returns:
            List of popular roles with counts
        """
        if not self.client:
            return []
        
        try:
            # Get all searches and count roles
            response = self.client.table("user_searches") \
                .select("target_role") \
                .execute()
            
            # Count occurrences
            role_counts: dict[str, int] = {}
            for record in response.data:
                if isinstance(record, dict):
                    role = str(record.get("target_role", "Unknown"))
                    role_counts[role] = role_counts.get(role, 0) + 1
            
            # Sort by count and return top roles
            sorted_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)
            return [{"role": role, "count": count} for role, count in sorted_roles[:limit]]
        except Exception as e:
            print(f"Error getting popular roles: {e}")
            return []
    
    def get_analytics_summary(self) -> dict[str, Any]:
        """
        Get summary analytics for admin dashboard.
        
        Returns:
            Dictionary with analytics data
        """
        if not self.client:
            return {}
        
        try:
            # Get total searches
            searches = self.client.table("user_searches").select("*").execute()
            
            # Get unique users
            unique_users: set[str] = set()
            for record in searches.data:
                if isinstance(record, dict):
                    user_id = record.get("user_id")
                    if user_id:
                        unique_users.add(str(user_id))
            
            return {
                "total_searches": len(searches.data),
                "unique_users": len(unique_users),
                "popular_roles": self.get_popular_roles(5)
            }
        except Exception as e:
            print(f"Error getting analytics: {e}")
            return {}


# Global tracker instance
_tracker = None

def get_tracker() -> SupabaseActivityTracker:
    """Get or create the global activity tracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = SupabaseActivityTracker()
    return _tracker
