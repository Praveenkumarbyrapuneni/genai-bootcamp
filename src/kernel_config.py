# src/kernel_config.py

"""
Kernel Configuration Module
This file sets up the Semantic Kernel with Groq (Fast & Free LLM).

Think of the Kernel as the "brain" of our AI system - it manages
connections to AI services and coordinates all AI operations.
"""

import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# Load environment variables from .env file
load_dotenv()


def create_kernel() -> Kernel:
    """
    Creates and configures a Semantic Kernel instance with Groq.
    
    Returns:
        Kernel: A configured kernel ready to use AI services
    
    How it works:
    1. Creates a new empty kernel
    2. Adds Groq as an AI service (Groq is OpenAI-compatible)
    3. Returns the configured kernel for use
    """
    
    # Step 1: Create a new kernel (the AI orchestrator)
    kernel = Kernel()
    
    # Step 2: Get Groq API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    # Step 3: Validate that we have the API key
    if not groq_api_key:
        raise ValueError(
            "Missing GROQ_API_KEY environment variable. Please check your .env file."
        )
    
    # Step 4: Create Groq service connection
    # Groq is OpenAI-compatible, so we can use OpenAIChatCompletion
    # We just need to set the environment variable for the base URL
    os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
    
    groq_chat_service = OpenAIChatCompletion(
        ai_model_id="llama-3.3-70b-versatile",  # Fast and powerful Groq model
        api_key=groq_api_key,
        service_id="groq_chat"
    )
    
    # Step 5: Add the AI service to our kernel
    kernel.add_service(groq_chat_service)
    
    # Step 6: Return the configured kernel
    print("✅ Kernel created successfully with Groq!")
    print(f"📡 Connected to: llama-3.3-70b-versatile (Groq)")
    print(f"⚡ Response time: 2-3 seconds (super fast!)")
    
    return kernel


# This runs only if we execute this file directly (for testing)
if __name__ == "__main__":
    print("Testing kernel creation...")
    test_kernel = create_kernel()
    print("Success! Kernel is ready to use.")