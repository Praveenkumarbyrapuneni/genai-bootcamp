# src/agents/base_agent.py

"""
Base Agent Class

This is the foundation for all specialized agents.
Each agent has:
- A name and role
- Specific expertise
- Access to kernel and tools
- Ability to communicate with other agents
"""

from typing import Dict, List, Optional
from semantic_kernel import Kernel


class BaseAgent:
    """
    Base class for all agents.
    
    What is an agent?
    - An AI with a specific role and expertise
    - Has personality and specialized knowledge
    - Can use specific tools
    - Communicates with other agents
    
    Think of it like hiring specialists for a team!
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        expertise: List[str],
        kernel: Kernel
    ):
        """
        Initialize base agent.
        
        Args:
            name: Agent's name (e.g., "Market Researcher")
            role: What they do (e.g., "Analyzes job markets")
            expertise: List of specialties
            kernel: Semantic Kernel for AI operations
        """
        self.name = name
        self.role = role
        self.expertise = expertise
        self.kernel = kernel
        
        # Agent's memory of conversations
        self.conversation_history = []
        
        print(f"🤖 {self.name} initialized")
        print(f"   Role: {self.role}")
        print(f"   Expertise: {', '.join(self.expertise)}")
    
    
    def get_system_prompt(self) -> str:
        """
        Get the agent's system prompt.
        
        This defines the agent's personality and expertise.
        Each specialized agent will override this.
        
        Returns:
            System prompt string
        """
        return f"""
You are {self.name}, a {self.role}.

Your expertise includes:
{chr(10).join(f"- {exp}" for exp in self.expertise)}

You are part of a multi-agent system helping users with career development.
Focus on your area of expertise and provide specific, actionable advice.
        """
    
    
    async def think(self, query: str, context: Optional[Dict] = None) -> str:
        """
        Agent thinks about a query.
        
        This is where the agent uses AI to process information
        and provide its expert opinion.
        
        Args:
            query: Question or task for the agent
            context: Additional context from other agents
        
        Returns:
            Agent's response
        """
        
        print(f"\n💭 {self.name} is thinking...")
        
        # Build prompt with context
        system_prompt = self.get_system_prompt()
        
        context_str = ""
        if context:
            context_str = "\n\nContext from other agents:\n"
            for agent_name, info in context.items():
                context_str += f"\n{agent_name}: {info}\n"
        
        full_prompt = f"""
{system_prompt}

{context_str}

Task: {query}

Provide your expert analysis and recommendations.
        """
        
        try:
            # Use kernel to get AI response
            result = await self.kernel.invoke_prompt(
                prompt=full_prompt,
                function_name=f"{self.name.lower().replace(' ', '_')}_think"
            )
            
            response = str(result).strip()
            
            # Store in conversation history
            self.conversation_history.append({
                "query": query,
                "response": response,
                "context": context
            })
            
            print(f"✅ {self.name} completed analysis")
            
            return response
            
        except Exception as e:
            print(f"❌ {self.name} error: {e}")
            return f"Error in {self.name}: {str(e)}"
    
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get agent's conversation history.
        
        Returns:
            List of past conversations
        """
        return self.conversation_history
    
    
    def __repr__(self) -> str:
        """String representation of agent."""
        return f"<Agent: {self.name} - {self.role}>"