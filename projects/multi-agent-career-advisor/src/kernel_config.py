# src/kernel_config.py

"""
Kernel Configuration Module
This file sets up the Semantic Kernel with Azure OpenAI.

Think of the Kernel as the "brain" of our AI system - it manages
connections to AI services and coordinates all AI operations.
"""

import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Load environment variables from .env file
# This reads the API keys we stored earlier
load_dotenv()


def create_kernel() -> Kernel:
    """
    Creates and configures a Semantic Kernel instance.
    
    Returns:
        Kernel: A configured kernel ready to use AI services
    
    How it works:
    1. Creates a new empty kernel
    2. Adds Azure OpenAI as an AI service
    3. Returns the configured kernel for use
    """
    
    # Step 1: Create a new kernel (the AI orchestrator)
    kernel = Kernel()
    
    # Step 2: Get credentials from environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    # Step 3: Validate that we have all required credentials
    if not endpoint or not api_key or not deployment_name:
        raise ValueError(
            "Missing required environment variables. Please check your .env file.\n"
            "Required: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME"
        )
    
    # Step 4: Create Azure OpenAI service connection
    # This is like creating a phone line to Azure's AI
    azure_chat_service = AzureChatCompletion(
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key
    )
    
    # Step 5: Add the AI service to our kernel
    # Now our kernel can use Azure OpenAI for responses
    kernel.add_service(azure_chat_service)
    
    # Step 6: Return the configured kernel
    print("✅ Kernel created successfully!")
    print(f"📡 Connected to: {deployment_name}")
    
    return kernel


# This runs only if we execute this file directly (for testing)
if __name__ == "__main__":
    print("Testing kernel creation...")
    test_kernel = create_kernel()
    print("Success! Kernel is ready to use.")