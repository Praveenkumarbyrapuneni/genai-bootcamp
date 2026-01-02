# src/auth/auth_manager.py

"""
Authentication Manager for CareerPath AI
Handles user registration, login, and session management.
Uses bcrypt for secure password hashing and Cosmos DB for user storage.
"""

import bcrypt
import streamlit as st
from datetime import datetime
import uuid
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.database.cosmos_manager import CareerDataManager


class AuthManager:
    """
    Manages user authentication for the CareerPath AI application.
    
    Features:
    - Secure password hashing with bcrypt
    - User registration and login
    - Session management with Streamlit
    - Integration with Cosmos DB for user storage
    """
    
    def __init__(self):
        """Initialize the auth manager with database connection."""
        self.db_manager = CareerDataManager()
        self._ensure_users_container()
    
    def _ensure_users_container(self):
        """Ensure the users container exists in Cosmos DB."""
        try:
            # Try to create users container if it doesn't exist
            self.db_manager.database.create_container_if_not_exists(
                id="users",
                partition_key={"paths": ["/email"], "kind": "Hash"}
            )
            self.users_container = self.db_manager.database.get_container_client("users")
        except Exception as e:
            print(f"Note: Using existing users container or fallback. {e}")
            try:
                self.users_container = self.db_manager.database.get_container_client("users")
            except:
                self.users_container = None
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password as string
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            hashed_password: Stored hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False
    
    def register_user(self, email: str, password: str, full_name: str) -> dict:
        """
        Register a new user.
        
        Args:
            email: User's email (used as unique identifier)
            password: User's password (will be hashed)
            full_name: User's full name
            
        Returns:
            dict with 'success' boolean and 'message' string
        """
        # Validate inputs
        if not email or not password or not full_name:
            return {"success": False, "message": "All fields are required."}
        
        if len(password) < 6:
            return {"success": False, "message": "Password must be at least 6 characters."}
        
        if "@" not in email:
            return {"success": False, "message": "Please enter a valid email address."}
        
        # Check if user already exists
        existing_user = self.get_user_by_email(email)
        if existing_user:
            return {"success": False, "message": "An account with this email already exists."}
        
        # Create new user
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "email": email.lower().strip(),
            "password_hash": self.hash_password(password),
            "full_name": full_name.strip(),
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None,
            "profile": {
                "target_role": "",
                "skills": [],
                "timeframe_months": 6
            }
        }
        
        try:
            if self.users_container:
                self.users_container.create_item(body=user_data)
            else:
                # Fallback: store in the main container with a type field
                user_data["type"] = "user"
                self.db_manager.container.create_item(body=user_data)
            
            return {"success": True, "message": "Account created successfully!", "user_id": user_id}
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
    
    def get_user_by_email(self, email: str) -> dict | None:
        """
        Retrieve a user by their email address.
        
        Args:
            email: User's email address
            
        Returns:
            User data dict or None if not found
        """
        email = email.lower().strip()
        
        try:
            if self.users_container:
                query = "SELECT * FROM c WHERE c.email = @email"
                params = [{"name": "@email", "value": email}]
                items = list(self.users_container.query_items(
                    query=query,
                    parameters=params,
                    enable_cross_partition_query=True
                ))
            else:
                # Fallback: query main container
                query = "SELECT * FROM c WHERE c.email = @email AND c.type = 'user'"
                params = [{"name": "@email", "value": email}]
                items = list(self.db_manager.container.query_items(
                    query=query,
                    parameters=params,
                    enable_cross_partition_query=True
                ))
            
            return items[0] if items else None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    
    def login(self, email: str, password: str) -> dict:
        """
        Authenticate a user.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            dict with 'success' boolean, 'message' string, and 'user' data if successful
        """
        if not email or not password:
            return {"success": False, "message": "Email and password are required."}
        
        user = self.get_user_by_email(email)
        
        if not user:
            return {"success": False, "message": "No account found with this email."}
        
        if not self.verify_password(password, user.get("password_hash", "")):
            return {"success": False, "message": "Incorrect password."}
        
        # Update last login
        try:
            user["last_login"] = datetime.utcnow().isoformat()
            if self.users_container:
                self.users_container.upsert_item(body=user)
            else:
                self.db_manager.container.upsert_item(body=user)
        except Exception:
            pass  # Non-critical, continue login
        
        # Return user data (without password hash)
        safe_user = {k: v for k, v in user.items() if k != "password_hash"}
        return {"success": True, "message": "Login successful!", "user": safe_user}
    
    def update_user_profile(self, user_id: str, email: str, profile_data: dict) -> bool:
        """
        Update user's profile data.
        
        Args:
            user_id: User's ID
            email: User's email (partition key)
            profile_data: New profile data to merge
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = self.get_user_by_email(email)
            if user:
                user["profile"] = {**user.get("profile", {}), **profile_data}
                if self.users_container:
                    self.users_container.upsert_item(body=user)
                else:
                    self.db_manager.container.upsert_item(body=user)
                return True
        except Exception as e:
            print(f"Error updating profile: {e}")
        return False


def init_session_state():
    """Initialize authentication-related session state variables."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"  # 'login' or 'register'


def logout():
    """Log out the current user."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.auth_page = "login"


def render_auth_page():
    """
    Render the authentication page (login/register).
    
    Returns:
        True if user is authenticated, False otherwise
    """
    init_session_state()
    
    # If already authenticated, return True
    if st.session_state.authenticated and st.session_state.user:
        return True
    
    auth_manager = AuthManager()
    
    # Center the auth form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🚀 CareerPath AI")
        st.markdown("#### Your AI-Powered Career Strategist")
        st.divider()
        
        # Toggle between login and register
        if st.session_state.auth_page == "login":
            st.markdown("### 🔐 Sign In")
            
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)
                
                if submit:
                    with st.spinner("Signing in..."):
                        result = auth_manager.login(email, password)
                    
                    if result["success"]:
                        st.session_state.authenticated = True
                        st.session_state.user = result["user"]
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])
            
            st.markdown("---")
            st.markdown("Don't have an account?")
            if st.button("Create Account", use_container_width=True):
                st.session_state.auth_page = "register"
                st.rerun()
                
        else:  # Register page
            st.markdown("### 📝 Create Account")
            
            with st.form("register_form"):
                full_name = st.text_input("Full Name", placeholder="John Doe")
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Min 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                
                submit = st.form_submit_button("Create Account", type="primary", use_container_width=True)
                
                if submit:
                    if password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        with st.spinner("Creating your account..."):
                            result = auth_manager.register_user(email, password, full_name)
                        
                        if result["success"]:
                            st.success(result["message"])
                            st.info("Please sign in with your new account.")
                            st.session_state.auth_page = "login"
                            st.rerun()
                        else:
                            st.error(result["message"])
            
            st.markdown("---")
            st.markdown("Already have an account?")
            if st.button("Sign In", use_container_width=True):
                st.session_state.auth_page = "login"
                st.rerun()
    
    return False
