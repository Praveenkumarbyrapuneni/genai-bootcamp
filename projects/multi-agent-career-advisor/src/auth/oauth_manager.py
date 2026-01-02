# src/auth/oauth_manager.py

"""
OAuth Authentication Manager for CareerPath AI
Uses Microsoft Entra ID (Azure AD) for professional authentication.
Supports Microsoft personal accounts and work/school accounts.
"""

import streamlit as st
import msal
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class OAuthConfig:
    """OAuth configuration for Microsoft Entra ID."""
    
    # Azure AD App Registration settings
    CLIENT_ID = os.getenv("AZURE_AD_CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("AZURE_AD_CLIENT_SECRET", "")
    TENANT_ID = os.getenv("AZURE_AD_TENANT_ID", "common")  # 'common' allows personal + work accounts
    
    # OAuth endpoints
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    
    # Redirect URI - update this for production
    REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8000")
    
    # Scopes - what permissions we're requesting
    SCOPES = ["User.Read", "openid", "profile", "email"]


class OAuthManager:
    """
    Manages OAuth 2.0 authentication with Microsoft Entra ID.
    
    Features:
    - Microsoft personal account login
    - Work/School account login
    - Secure token management
    - User profile retrieval
    """
    
    def __init__(self):
        """Initialize the MSAL confidential client."""
        self.config = OAuthConfig()
        
        if self.config.CLIENT_ID and self.config.CLIENT_SECRET:
            self.app = msal.ConfidentialClientApplication(
                client_id=self.config.CLIENT_ID,
                client_credential=self.config.CLIENT_SECRET,
                authority=self.config.AUTHORITY
            )
        else:
            self.app = None
    
    def get_auth_url(self) -> str:
        """
        Generate the Microsoft login URL.
        
        Returns:
            Authorization URL to redirect user to Microsoft login
        """
        if not self.app:
            return ""
        
        # Generate a unique state for CSRF protection
        state = str(uuid.uuid4())
        st.session_state["oauth_state"] = state
        
        auth_url = self.app.get_authorization_request_url(
            scopes=self.config.SCOPES,
            state=state,
            redirect_uri=self.config.REDIRECT_URI
        )
        return auth_url
    
    def get_token_from_code(self, auth_code: str) -> dict | None:
        """
        Exchange authorization code for access token.
        
        Args:
            auth_code: The authorization code from Microsoft callback
            
        Returns:
            Token response dict or None if failed
        """
        if not self.app:
            return None
        
        try:
            result = self.app.acquire_token_by_authorization_code(
                code=auth_code,
                scopes=self.config.SCOPES,
                redirect_uri=self.config.REDIRECT_URI
            )
            return result if "access_token" in result else None
        except Exception as e:
            print(f"Token acquisition failed: {e}")
            return None
    
    def get_user_info(self, access_token: str) -> dict | None:
        """
        Fetch user profile from Microsoft Graph API.
        
        Args:
            access_token: Valid access token
            
        Returns:
            User profile dict or None if failed
        """
        import httpx
        
        try:
            response = httpx.get(
                "https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Failed to get user info: {e}")
        return None


def init_oauth_session_state():
    """Initialize OAuth-related session state variables."""
    if "oauth_authenticated" not in st.session_state:
        st.session_state.oauth_authenticated = False
    if "oauth_user" not in st.session_state:
        st.session_state.oauth_user = None
    if "oauth_token" not in st.session_state:
        st.session_state.oauth_token = None


def oauth_logout():
    """Log out the current OAuth user."""
    st.session_state.oauth_authenticated = False
    st.session_state.oauth_user = None
    st.session_state.oauth_token = None
    # Clear query params
    st.query_params.clear()


def handle_oauth_callback():
    """
    Handle the OAuth callback from Microsoft.
    Processes the authorization code and retrieves user info.
    """
    query_params = st.query_params
    
    # Check if this is a callback with an auth code
    if "code" in query_params:
        auth_code = query_params.get("code")
        
        oauth_manager = OAuthManager()
        token_result = oauth_manager.get_token_from_code(auth_code)
        
        if token_result:
            # Get user info from Microsoft Graph
            user_info = oauth_manager.get_user_info(token_result["access_token"])
            
            if user_info:
                st.session_state.oauth_authenticated = True
                st.session_state.oauth_token = token_result
                st.session_state.oauth_user = {
                    "id": user_info.get("id"),
                    "email": user_info.get("mail") or user_info.get("userPrincipalName"),
                    "full_name": user_info.get("displayName"),
                    "first_name": user_info.get("givenName"),
                    "last_name": user_info.get("surname"),
                    "job_title": user_info.get("jobTitle"),
                    "login_time": datetime.utcnow().isoformat()
                }
                # Clear the code from URL
                st.query_params.clear()
                return True
    
    return False


def render_oauth_login_page() -> bool:
    """
    Render the OAuth login page.
    
    Returns:
        True if user is authenticated, False otherwise
    """
    init_oauth_session_state()
    
    # Handle OAuth callback if present
    handle_oauth_callback()
    
    # If already authenticated, return True
    if st.session_state.oauth_authenticated and st.session_state.oauth_user:
        return True
    
    oauth_manager = OAuthManager()
    
    # Check if OAuth is configured
    if not oauth_manager.app:
        st.error("⚠️ OAuth not configured. Please set up Azure AD credentials in .env file.")
        st.code("""
# Add these to your .env file:
AZURE_AD_CLIENT_ID=your-client-id
AZURE_AD_CLIENT_SECRET=your-client-secret
AZURE_AD_TENANT_ID=common
OAUTH_REDIRECT_URI=http://localhost:8000
        """)
        st.info("📖 See instructions below to set up Azure AD App Registration")
        
        with st.expander("🔧 How to set up Microsoft Entra ID (Azure AD)"):
            st.markdown("""
            ### Step 1: Register an App in Azure Portal
            1. Go to [Azure Portal](https://portal.azure.com)
            2. Navigate to **Microsoft Entra ID** → **App registrations**
            3. Click **New registration**
            4. Name: `CareerPath AI`
            5. Supported account types: **Personal Microsoft accounts and organizational accounts**
            6. Redirect URI: `http://localhost:8000` (Web)
            7. Click **Register**
            
            ### Step 2: Get Your Credentials
            1. Copy the **Application (client) ID** → `AZURE_AD_CLIENT_ID`
            2. Copy the **Directory (tenant) ID** → `AZURE_AD_TENANT_ID` (or use `common`)
            3. Go to **Certificates & secrets** → **New client secret**
            4. Copy the secret value → `AZURE_AD_CLIENT_SECRET`
            
            ### Step 3: Configure API Permissions
            1. Go to **API permissions**
            2. Add: `Microsoft Graph` → `User.Read`, `openid`, `profile`, `email`
            3. Click **Grant admin consent** (if you're an admin)
            
            ### Step 4: Update .env file
            Add the credentials to your `.env` file and restart the app.
            """)
        
        return False
    
    # Center the login UI
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🚀 CareerPath AI")
        st.markdown("#### Your AI-Powered Career Strategist")
        st.divider()
        
        st.markdown("### 🔐 Sign In")
        st.markdown("Use your Microsoft account to continue")
        
        # Microsoft Sign-In Button
        auth_url = oauth_manager.get_auth_url()
        
        st.markdown(f"""
        <a href="{auth_url}" target="_self">
            <button style="
                background-color: #2F2F2F;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                display: flex;
                align-items: center;
                gap: 10px;
                width: 100%;
                justify-content: center;
                margin: 20px 0;
            ">
                <img src="https://learn.microsoft.com/en-us/entra/identity-platform/media/howto-add-branding-in-apps/ms-symbollockup_mssymbol_19.svg" 
                     width="20" height="20" style="background: white; padding: 2px; border-radius: 2px;">
                Sign in with Microsoft
            </button>
        </a>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.caption("🔒 Secure authentication powered by Microsoft Entra ID")
        st.caption("Your credentials are never stored in our application")
    
    return False
