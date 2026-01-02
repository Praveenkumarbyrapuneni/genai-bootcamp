# dashboard/app.py

import streamlit as st
import sys
import os
import asyncio
import pandas as pd
import plotly.express as px
import json

# 1. Add project root to path so we can import our src modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.career_advisor import CareerAdvisorAgent
from src.database.cosmos_manager import CareerDataManager
from src.kernel_config import create_kernel
from src.auth.supabase_auth import render_supabase_login, supabase_logout, init_supabase_session

# 2. Configure the Page
st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🚀",
    layout="wide"
)

# 3. Initialize session state and check authentication
init_supabase_session()

# 4. Show login page if not authenticated
if not render_supabase_login():
    st.stop()  # Stop execution here if not authenticated

# ============================================
# AUTHENTICATED USER CONTENT BELOW
# ============================================

# Get current user info from session state
current_user = st.session_state.supabase_user
user_id = current_user["id"]
user_name = current_user.get("full_name") or current_user["email"].split("@")[0]
user_email = current_user["email"]
avatar_url = current_user.get("avatar_url", "")

# Header with user info and logout
col_title, col_user = st.columns([3, 1])

with col_title:
    st.title("🚀 CareerPath AI")
    st.markdown("### Your Multi-Agent Career Strategist")

with col_user:
    if avatar_url:
        st.image(avatar_url, width=50)
    st.markdown(f"**👤 {user_name}**")
    st.caption(user_email)
    if st.button("🚪 Logout", use_container_width=True):
        supabase_logout()
        st.rerun()

st.divider()

# 5. Sidebar for User Inputs
with st.sidebar:
    first_name = user_name.split()[0] if user_name else "User"
    st.header(f"👤 Welcome, {first_name}!")
    
    st.divider()
    
    target_role = st.text_input(
        "Target Role", 
        value="Senior GenAI Engineer"
    )
    
    # Load skills dynamically from a JSON file
    skills_file_path = os.path.join(os.path.dirname(__file__), '../prompts/skills_analyzer/skills.json')
    try:
        with open(skills_file_path, 'r') as f:
            all_skills = json.load(f)
    except FileNotFoundError:
        all_skills = ["Python", "Semantic Kernel", "Azure OpenAI", "Basic SQL", "Machine Learning", "Data Analysis", "Cloud Computing", "Java", "JavaScript", "React", "Node.js", "LLM", "Prompt Engineering", "Data Science", "DevOps", "Cybersecurity"]

    # Enhanced multiselect with fallback for user input
    skills_input = st.multiselect(
        "Current Skills",
        options=all_skills,
        default=["Python", "Semantic Kernel", "Azure OpenAI", "Basic SQL"],
        help="Select your current skills from the list or type to add new ones."
    )

    # Allow user to add custom skills
    custom_skill = st.text_input("Add a custom skill", "")
    if custom_skill and custom_skill not in skills_input:
        skills_input.append(custom_skill)

    current_skills = skills_input
    
    timeframe = st.slider("Goal Timeline (Months)", 1, 12, 6)
    
    st.divider()
    
    # History Toggle
    if st.checkbox("📜 Show Analysis History"):
        st.session_state['show_history'] = True
    else:
        st.session_state['show_history'] = False
    
    st.divider()
    
    # Account info
    provider = current_user.get("provider", "")
    if provider:
        st.caption(f"🔗 Signed in via {provider.title()}")
    st.caption("📧 " + user_email)

# 6. Main Action Button
if st.button("🤖 Start Career Analysis", type="primary"):
    
    # Progress Bar & Status
    progress_text = "Initializing AI Agents..."
    my_bar = st.progress(0, text=progress_text)
    
    try:
        # A. Initialize System
        kernel = create_kernel()
        advisor = CareerAdvisorAgent(kernel)
        db_manager = CareerDataManager()
        
        # B. Run Analysis (Async wrapper)
        async def run_analysis():
            my_bar.progress(25, text="🕵️ Market Researcher is scraping trends...")
            
            result = await advisor.comprehensive_career_analysis(
                target_role=target_role,
                current_skills=current_skills,
                timeframe_months=timeframe
            )
            return result
        
        # Run the async function
        results = asyncio.run(run_analysis())
        my_bar.progress(75, text="💾 Saving results to Azure Cosmos DB...")
        
        # C. Save to Cloud Database
        db_manager.save_career_analysis(
            user_id=user_id,
            role=target_role,
            analysis_data=results
        )
        
        my_bar.progress(100, text="✅ Analysis Complete!")
        
        # D. Display Results
        st.success("New Career Strategy Generated!")
        
        # Tabs for different agents
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏆 Recommendation", 
            "📊 Market Data", 
            "🎓 Learning Plan", 
            "📝 Strategy"
        ])
        
        with tab1:
            st.markdown("### 🎯 Executive Summary")
            st.markdown(results.get("final_recommendations", "No summary available."))
            
        with tab2:
            st.markdown("### 🕵️ Market Intelligence")
            st.info(results.get("market_research", "No data."))
            
        with tab3:
            st.markdown("### 📚 Personalized Curriculum")
            st.warning(results.get("learning_plan", "No plan generated."))
            
        with tab4:
            st.markdown("### 💼 Application Strategy")
            st.markdown(results.get("application_strategy", "No strategy found."))
            
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")

# 7. History Section (Reads from Azure Cosmos DB)
if st.session_state.get('show_history'):
    st.divider()
    st.subheader(f"📜 Your Analysis History")
    
    try:
        db = CareerDataManager()
        history = db.get_user_history(user_id)
        
        if history:
            st.caption(f"Found {len(history)} past analyses in cloud storage.")
            
            for item in history:
                # Format timestamp nicely
                ts = item['timestamp'].split('T')[0]
                role = item.get('target_role', 'Unknown Role')
                
                with st.expander(f"📅 {ts}: {role}"):
                    # Show the saved data
                    data = item.get('data', {})
                    st.write(data.get('final_recommendations', 'No summary saved.'))
                    if st.button("Load Full Report", key=item['id']):
                        st.json(data)
        else:
            st.info("No history found. Run your first career analysis!")
            
    except Exception as e:
        st.error(f"Could not load history: {e}")