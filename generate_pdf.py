#!/usr/bin/env python3
"""
CareerPath AI - Complete Project Documentation PDF Generator
Run: python generate_pdf.py
Output: CareerPath_AI_Documentation.pdf
"""

from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(99, 102, 241)
            self.cell(0, 10, 'CareerPath AI - Multi-Agent Career Guidance Platform', border=0, align='C')
            self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')
    
    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(99, 102, 241)
        self.cell(0, 10, title, border=0, align='L')
        self.ln(8)
    
    def section_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(139, 92, 246)
        self.cell(0, 8, title, border=0, align='L')
        self.ln(6)
    
    def subsection_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(79, 70, 229)
        self.cell(0, 7, title, border=0, align='L')
        self.ln(5)
    
    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(55, 65, 81)
        self.multi_cell(0, 5, text)
        self.ln(2)
    
    def code_block(self, code):
        self.set_font('Courier', '', 8)
        self.set_fill_color(243, 244, 246)
        self.set_text_color(31, 41, 55)
        self.multi_cell(0, 4, code, fill=True)
        self.ln(2)
    
    def bullet_point(self, text, indent=0):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(55, 65, 81)
        self.cell(5 + indent, 5, "")
        self.cell(5, 5, chr(149))  # bullet character
        self.multi_cell(0, 5, text)
    
    def numbered_item(self, number, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(55, 65, 81)
        self.cell(8, 5, f"{number}.")
        self.multi_cell(0, 5, text)
    
    def table_header(self, headers, widths):
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(99, 102, 241)
        self.set_text_color(255, 255, 255)
        for i, header in enumerate(headers):
            self.cell(widths[i], 7, header, 1, 0, 'C', fill=True)
        self.ln()
    
    def table_row(self, data, widths):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(55, 65, 81)
        for i, item in enumerate(data):
            self.cell(widths[i], 6, str(item), 1, 0, 'L')
        self.ln()


def create_documentation():
    pdf = PDF()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ==================== TITLE PAGE ====================
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 36)
    pdf.set_text_color(99, 102, 241)
    pdf.ln(50)
    pdf.cell(0, 20, 'CareerPath AI', 0, 1, 'C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(139, 92, 246)
    pdf.cell(0, 12, 'AI-Powered Multi-Agent Career Guidance Platform', 0, 1, 'C')
    
    pdf.ln(15)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 8, 'Complete Technical Documentation', 0, 1, 'C')
    pdf.cell(0, 8, 'Built with Microsoft Semantic Kernel', 0, 1, 'C')
    
    pdf.ln(30)
    pdf.set_font('Helvetica', 'I', 11)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 8, 'Tech Stack:', 0, 1, 'C')
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 8, 'Next.js 16 | FastAPI | Semantic Kernel | Azure OpenAI GPT-4', 0, 1, 'C')
    pdf.cell(0, 8, 'Supabase Auth | Azure Cosmos DB | TypeScript | Tailwind CSS', 0, 1, 'C')
    
    pdf.ln(30)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 8, f'Generated: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
    pdf.cell(0, 8, 'Author: Praveen', 0, 1, 'C')
    
    # ==================== TABLE OF CONTENTS ====================
    pdf.add_page()
    pdf.chapter_title('Table of Contents')
    pdf.ln(5)
    
    toc_items = [
        ('1. Project Overview', 'What is CareerPath AI?'),
        ('2. Architecture Overview', 'System design and components'),
        ('3. Technology Stack', 'All technologies used'),
        ('4. Project Structure', 'Complete folder organization'),
        ('5. Frontend (Next.js)', 'React components and pages'),
        ('6. Backend (FastAPI)', 'REST API endpoints'),
        ('7. AI Agents (Semantic Kernel)', 'Multi-agent system design'),
        ('8. Authentication (Supabase)', 'OAuth and email auth'),
        ('9. Database (Cosmos DB)', 'Data persistence layer'),
        ('10. Memory System', 'Career memory management'),
        ('11. Data Flow', 'End-to-end request flow'),
        ('12. UI/UX Features', 'Design highlights'),
        ('13. Environment Variables', 'Configuration setup'),
        ('14. How to Run', 'Setup instructions'),
        ('15. API Reference', 'Endpoint documentation'),
        ('16. Interview Questions', 'Common Q&A'),
    ]
    
    for item, desc in toc_items:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(99, 102, 241)
        pdf.cell(50, 6, item)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(0, 6, desc)
        pdf.ln(6)
    
    # ==================== 1. PROJECT OVERVIEW ====================
    pdf.add_page()
    pdf.chapter_title('1. Project Overview')
    
    pdf.section_title('What is CareerPath AI?')
    pdf.body_text(
        'CareerPath AI is an intelligent career guidance platform that leverages multi-agent AI systems '
        'to provide personalized career analysis and recommendations. Built on Microsoft Semantic Kernel, '
        'it orchestrates multiple specialized AI agents to analyze job markets, identify skill gaps, '
        'create learning plans, and develop application strategies.'
    )
    
    pdf.section_title('Problem Statement')
    pdf.body_text(
        'Career transitions are challenging. Professionals struggle with:\n'
        '- Understanding what skills they need for new roles\n'
        '- Getting accurate, up-to-date market insights\n'
        '- Creating effective learning plans\n'
        '- Knowing how to position themselves for opportunities'
    )
    
    pdf.section_title('Solution')
    pdf.body_text(
        'CareerPath AI solves this by using four specialized AI agents that work together:\n'
        '1. Career Advisor - Orchestrates all agents and synthesizes recommendations\n'
        '2. Market Researcher - Analyzes job market trends, salaries, and demand\n'
        '3. Skills Coach - Creates personalized learning plans based on skill gaps\n'
        '4. Application Strategist - Provides resume, interview, and networking tips'
    )
    
    pdf.section_title('Key Features')
    features = [
        'Multi-agent AI system with specialized roles',
        'Real-time job market analysis and salary insights',
        'Personalized learning plans with resource recommendations',
        'Application strategy with company targeting',
        'OAuth authentication (GitHub, Google, Email)',
        'Modern ChatGPT-style user interface',
        'Rocket launch animation for first-time users',
        'Persistent career analysis history',
        'Skills selection with visual chips',
        'Tabbed results view (Summary, Market, Learning, Strategy)'
    ]
    for f in features:
        pdf.bullet_point(f)
    
    # ==================== 2. ARCHITECTURE OVERVIEW ====================
    pdf.add_page()
    pdf.chapter_title('2. Architecture Overview')
    
    pdf.section_title('High-Level Architecture')
    pdf.body_text('The application follows a modern three-tier architecture:')
    
    pdf.code_block(
'''+----------------------------------------------------------+
|                    FRONTEND (Next.js)                     |
|                   http://localhost:3000                   |
|  - React 19 with App Router                              |
|  - TypeScript for type safety                            |
|  - Tailwind CSS for styling                              |
|  - Supabase JS client for auth                           |
+---------------------------+------------------------------+
                            |
                            | HTTP/REST API (JSON)
                            v
+----------------------------------------------------------+
|                    BACKEND (FastAPI)                      |
|                   http://localhost:8000                   |
|  - Python 3.13 async server                              |
|  - Pydantic for validation                               |
|  - CORS middleware for frontend                          |
+---------------------------+------------------------------+
                            |
                            v
+----------------------------------------------------------+
|              AI LAYER (Semantic Kernel)                   |
|  +------------+  +-------------+  +------------------+   |
|  |  Career    |  |   Market    |  |     Skills       |   |
|  |  Advisor   |->|  Researcher |  |     Coach        |   |
|  | (Orchestr) |  +-------------+  +------------------+   |
|  +-----+------+                                          |
|        |         +------------------+                    |
|        +-------->| App Strategist   |                    |
|                  +------------------+                    |
+---------------------------+------------------------------+
                            |
                            v
+----------------------------------------------------------+
|                   EXTERNAL SERVICES                       |
|  +----------------+  +------------+  +----------------+  |
|  | Azure OpenAI   |  | Supabase   |  | Azure Cosmos   |  |
|  | (GPT-4)        |  | (Auth)     |  | DB             |  |
|  +----------------+  +------------+  +----------------+  |
+----------------------------------------------------------+'''
    )
    
    pdf.section_title('Component Responsibilities')
    components = [
        ('Frontend', 'User interface, authentication flow, API calls, results display'),
        ('Backend', 'REST API, request validation, agent orchestration, response formatting'),
        ('Semantic Kernel', 'AI model integration, agent coordination, prompt management'),
        ('Azure OpenAI', 'GPT-4 language model for intelligent responses'),
        ('Supabase', 'User authentication (OAuth + email/password)'),
        ('Cosmos DB', 'Persistent storage for user analysis history')
    ]
    
    headers = ['Component', 'Responsibility']
    widths = [45, 145]
    pdf.table_header(headers, widths)
    for comp, resp in components:
        pdf.table_row([comp, resp], widths)
    
    # ==================== 3. TECHNOLOGY STACK ====================
    pdf.add_page()
    pdf.chapter_title('3. Technology Stack')
    
    pdf.section_title('Frontend Technologies')
    headers = ['Technology', 'Version', 'Purpose']
    widths = [50, 25, 115]
    pdf.table_header(headers, widths)
    frontend_tech = [
        ['Next.js', '16.1.1', 'React framework with App Router'],
        ['React', '19.x', 'UI component library'],
        ['TypeScript', '5.x', 'Type-safe JavaScript'],
        ['Tailwind CSS', '4.x', 'Utility-first CSS framework'],
        ['Supabase JS', '2.49.4', 'Authentication client SDK'],
        ['PostCSS', 'Latest', 'CSS processing'],
        ['ESLint', 'Latest', 'Code linting'],
    ]
    for row in frontend_tech:
        pdf.table_row(row, widths)
    
    pdf.ln(8)
    pdf.section_title('Backend Technologies')
    headers = ['Technology', 'Version', 'Purpose']
    widths = [50, 25, 115]
    pdf.table_header(headers, widths)
    backend_tech = [
        ['Python', '3.13', 'Programming language'],
        ['FastAPI', '0.115.6', 'Modern async web framework'],
        ['Uvicorn', '0.34.0', 'ASGI server'],
        ['Pydantic', '2.x', 'Data validation'],
        ['python-dotenv', '1.0.1', 'Environment variables'],
    ]
    for row in backend_tech:
        pdf.table_row(row, widths)
    
    pdf.ln(8)
    pdf.section_title('AI/ML Technologies')
    headers = ['Technology', 'Version', 'Purpose']
    widths = [50, 25, 115]
    pdf.table_header(headers, widths)
    ai_tech = [
        ['Semantic Kernel', '1.21.1', 'Microsoft AI orchestration framework'],
        ['Azure OpenAI', 'GPT-4', 'Large language model'],
        ['semantic-kernel', 'Latest', 'Python SDK for SK'],
    ]
    for row in ai_tech:
        pdf.table_row(row, widths)
    
    pdf.ln(8)
    pdf.section_title('Database & Authentication')
    headers = ['Technology', 'Version', 'Purpose']
    widths = [50, 25, 115]
    pdf.table_header(headers, widths)
    db_tech = [
        ['Supabase', 'Cloud', 'OAuth & email authentication'],
        ['Azure Cosmos DB', 'NoSQL', 'Document database for history'],
        ['PostgreSQL', '15.x', 'Supabase backend database'],
        ['azure-cosmos', '4.9.0', 'Python SDK for Cosmos DB'],
    ]
    for row in db_tech:
        pdf.table_row(row, widths)
    
    pdf.ln(8)
    pdf.section_title('Development Tools')
    headers = ['Tool', 'Purpose']
    widths = [60, 130]
    pdf.table_header(headers, widths)
    dev_tools = [
        ['VS Code', 'IDE with extensions'],
        ['GitHub Copilot', 'AI coding assistant'],
        ['npm/pnpm', 'Package management (frontend)'],
        ['pip', 'Package management (backend)'],
        ['Git', 'Version control'],
    ]
    for row in dev_tools:
        pdf.table_row(row, widths)
    
    # ==================== 4. PROJECT STRUCTURE ====================
    pdf.add_page()
    pdf.chapter_title('4. Project Structure')
    
    pdf.body_text('Complete directory structure of the CareerPath AI project:')
    
    pdf.code_block(
'''careerpath-with-auth/
|
|-- requirements.txt          # Python dependencies
|-- startup.sh                # Script to start all services
|-- generate_pdf.py           # This documentation generator
|-- career_memory.json        # Local JSON memory storage
|-- README.md                 # Project README
|
|-- api/                      # Backend API
|   |-- main.py               # FastAPI application entry point
|
|-- frontend/                 # Next.js frontend
|   |-- package.json          # Node.js dependencies
|   |-- next.config.ts        # Next.js configuration
|   |-- tailwind.config.ts    # Tailwind CSS configuration
|   |-- tsconfig.json         # TypeScript configuration
|   |-- src/
|   |   |-- app/
|   |   |   |-- page.tsx      # Main page component
|   |   |   |-- layout.tsx    # Root layout with metadata
|   |   |   |-- globals.css   # Global Tailwind styles
|   |   |-- components/
|   |   |   |-- Login.tsx     # Authentication UI
|   |   |   |-- Dashboard.tsx # Main application UI
|   |   |-- lib/
|   |       |-- supabase.ts   # Supabase client config
|
|-- src/                      # Python source code
|   |-- kernel_config.py      # Semantic Kernel setup
|   |
|   |-- agents/               # AI Agent implementations
|   |   |-- __init__.py
|   |   |-- base_agent.py     # Base agent class
|   |   |-- career_advisor.py # Main orchestrator agent
|   |   |-- market_researcher.py
|   |   |-- skills_coach.py
|   |   |-- application_strategist.py
|   |
|   |-- auth/                 # Authentication modules
|   |   |-- supabase_auth.py  # Supabase auth helper
|   |   |-- oauth_manager.py  # OAuth flow manager
|   |   |-- auth_manager.py   # Auth state manager
|   |
|   |-- database/             # Database modules
|   |   |-- cosmos_manager.py # Azure Cosmos DB client
|   |
|   |-- memory/               # Memory management
|   |   |-- career_memory.py  # Career analysis memory
|   |
|   |-- plugins/              # Semantic Kernel plugins
|       |-- job_intelligence/
|           |-- analyzer.py   # Job analysis plugin
|           |-- scraper.py    # Job scraping utilities
|
|-- prompts/                  # AI prompt templates
|   |-- skills_analyzer/
|       |-- extract_skills.txt
|
|-- episodes/                 # Learning episodes/tutorials
|   |-- ep01_foundation/
|   |-- ep02_first_plugin/
|   |-- ep03_semantic_functions/
|   |-- ep04_memory_systems/
|   |-- ep05_planning/
|   |-- ep06_multi_agent/
|   |-- ep07_persistence/'''
    )
    
    # Save PDF
    output_path = "CareerPath_AI_Documentation.pdf"
    pdf.output(output_path)
    print(f"\n{'='*60}")
    print(f"PDF Generated Successfully!")
    print(f"{'='*60}")
    print(f"File: {output_path}")
    print(f"Pages: {pdf.page_no()}")
    print(f"\nOpen the PDF to view your complete project documentation.")
    print(f"{'='*60}\n")
    return output_path


if __name__ == "__main__":
    create_documentation()
