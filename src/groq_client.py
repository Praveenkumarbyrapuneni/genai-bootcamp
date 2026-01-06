"""
Groq Client for Fast LLM Responses
This replaces Semantic Kernel with direct Groq API calls for speed.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    """Fast LLM client using Groq API"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        print(f"✅ Groq client initialized with {self.model}")
    
    async def get_completion(self, prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> str:
        """Get completion from Groq"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        return response.choices[0].message.content

# Create a singleton instance
_groq_client = None

def get_groq_client() -> GroqClient:
    """Get or create the Groq client singleton"""
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqClient()
    return _groq_client
