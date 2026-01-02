# Episode 7: Multi-Agent System Architecture

**Date:** [Current Date]
**Status:** ✅ Complete
**Tech Stack:** Semantic Kernel, Python, AsyncIO

## 🎯 Goal
Move beyond single-prompt interactions to create a **team of specialized AI agents** that collaborate to solve complex career problems. Instead of one "Generic AI" trying to do everything, we utilize an **Orchestrator-Workers** pattern.

## 🏗️ The Agent Team
We built an Object-Oriented system with one base class and four specialized agents:

| Agent Name | Role | Responsibility |
|------------|------|----------------|
| **Career Advisor** | 🎻 Orchestrator | The "Manager." Receives user request, delegates tasks to specialists, and synthesizes the final report. |
| **Market Researcher** | 📊 Specialist | Analyzes job trends, demand, and salary data. |
| **Skills Coach** | 🎓 Specialist | Compares user profile vs. market data to find gaps and create learning plans. |
| **Application Strategist** | 📝 Specialist | Optimizes resumes and creates application strategies based on the specific role. |

## 🧩 Architecture

```mermaid
graph TD
    User[User Request] --> Advisor[Career Advisor Agent]
    Advisor -->|Delegate: Analyze Trends| Researcher[Market Researcher]
    Advisor -->|Delegate: Check Gaps| Coach[Skills Coach]
    Advisor -->|Delegate: Plan Strategy| Strategist[Application Strategist]
    
    Researcher -->|Market Data| Advisor
    Coach -->|Learning Plan| Advisor
    Strategist -->|App Tactics| Advisor
    
    Advisor -->|Synthesize & Report| Final[Comprehensive Career Plan]