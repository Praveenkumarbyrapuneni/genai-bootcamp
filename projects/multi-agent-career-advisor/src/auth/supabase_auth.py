# src/auth/supabase_auth.py

"""
Supabase Authentication Manager for CareerPath AI
Supports GitHub, Google, and other OAuth providers.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class SupabaseAuth:
    """
    Manages OAuth authentication using Supabase.
    
    Features:
    - GitHub login
    - Google login (if enabled)
    - Session management
    - User profile retrieval
    """
    
    def __init__(self):
        """Initialize Supabase client."""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        
        if self.url and self.key:
            self.client: Client = create_client(self.url, self.key)
        else:
            self.client = None
    
    def get_oauth_url(self, provider: str = "github") -> str:
        """
        Get OAuth login URL for the specified provider.
        
        Args:
            provider: OAuth provider ('github', 'google', etc.)
            
        Returns:
            OAuth URL to redirect user to
        """
        if not self.client:
            return ""
        
        try:
            # Get the redirect URL (your app URL)
            redirect_url = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8000")
            
            response = self.client.auth.sign_in_with_oauth({
                "provider": provider,
                "options": {
                    "redirect_to": redirect_url
                }
            })
            return response.url
        except Exception as e:
            print(f"Error getting OAuth URL: {e}")
            return ""
    
    def get_session_from_url(self, access_token: str, refresh_token: str) -> dict | None:
        """
        Set session using tokens from URL callback.
        
        Args:
            access_token: Access token from URL
            refresh_token: Refresh token from URL
            
        Returns:
            Session data or None
        """
        if not self.client:
            return None
        
        try:
            response = self.client.auth.set_session(access_token, refresh_token)
            return response
        except Exception as e:
            print(f"Error setting session: {e}")
            return None
    
    def get_user(self) -> dict | None:
        """
        Get current logged-in user.
        
        Returns:
            User data or None
        """
        if not self.client:
            return None
        
        try:
            response = self.client.auth.get_user()
            if response and response.user:
                user = response.user
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.user_metadata.get("full_name") or user.user_metadata.get("name", ""),
                    "avatar_url": user.user_metadata.get("avatar_url", ""),
                    "provider": user.app_metadata.get("provider", ""),
                }
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def sign_out(self):
        """Sign out the current user."""
        if self.client:
            try:
                self.client.auth.sign_out()
            except Exception as e:
                print(f"Error signing out: {e}")


def init_supabase_session():
    """Initialize Supabase session state."""
    if "supabase_authenticated" not in st.session_state:
        st.session_state.supabase_authenticated = False
    if "supabase_user" not in st.session_state:
        st.session_state.supabase_user = None


def supabase_logout():
    """Log out from Supabase."""
    auth = SupabaseAuth()
    auth.sign_out()
    st.session_state.supabase_authenticated = False
    st.session_state.supabase_user = None
    st.query_params.clear()


def handle_oauth_callback():
    """Handle OAuth callback from Supabase."""
    query_params = st.query_params
    
    # Check for access_token in URL (Supabase OAuth callback)
    if "access_token" in query_params and "refresh_token" in query_params:
        access_token = query_params.get("access_token")
        refresh_token = query_params.get("refresh_token")
        
        auth = SupabaseAuth()
        session = auth.get_session_from_url(access_token, refresh_token)
        
        if session:
            user = auth.get_user()
            if user:
                st.session_state.supabase_authenticated = True
                st.session_state.supabase_user = user
                st.query_params.clear()
                return True
    
    return False


def render_supabase_login() -> bool:
    """
    Render Supabase OAuth login page.
    
    Returns:
        True if authenticated, False otherwise
    """
    init_supabase_session()
    
    # Handle OAuth callback
    handle_oauth_callback()
    
    # Already authenticated
    if st.session_state.supabase_authenticated and st.session_state.supabase_user:
        return True
    
    auth = SupabaseAuth()
    
    # Check if Supabase is configured
    if not auth.client:
        st.error("⚠️ Supabase not configured. Check your .env file.")
        return False
    
    # Center the login UI
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🚀 CareerPath AI")
        st.markdown("#### Your AI-Powered Career Strategist")
        st.divider()
        
        st.markdown("### 🔐 Sign In")
        st.markdown("Choose your preferred login method")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # GitHub Login Button
        github_url = auth.get_oauth_url("github")
        if github_url:
            st.markdown(f"""
            <a href="{github_url}" target="_self" style="text-decoration: none;">
                <div style="
                    background-color: #24292e;
                    color: white;
                    padding: 12px 24px;
                    border-radius: 6px;
                    text-align: center;
                    font-size: 16px;
                    font-weight: 500;
                    margin: 10px 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                ">
                    <svg height="20" width="20" viewBox="0 0 16 16" fill="white">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                    </svg>
                    Continue with GitHub
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.divider()
        
        st.caption("🔒 Secure authentication powered by Supabase")
        st.caption("We never store your password")
    
    return False
