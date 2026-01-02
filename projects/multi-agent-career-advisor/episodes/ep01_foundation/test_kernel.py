# episodes/ep01_foundation/test_kernel.py

"""
Episode 1: First AI Interaction
This script tests our kernel by having a simple conversation with AI.
"""

import asyncio
import sys
import os

# Add the src directory to Python's path so we can import our kernel_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.kernel_config import create_kernel


async def first_ai_conversation():
    """
    MY first AI conversation using Semantic Kernel!
    
    'async' means this function can wait for responses without freezing.
    AI calls take time (network request to Azure), so we use async.
    """
    
    print("🚀 Starting Episode 1: First AI Conversation\n")
    
    # Step 1: Create our kernel
    print("📦 Creating kernel...")
    kernel = create_kernel()
    
    # Step 2: Prepare MY prompt (question for the AI)
    prompt = """
    You are a career advisor for GenAI engineers. 
    A student just learned Semantic Kernel and wants to build an AI agent.
    
    In 2-3 sentences, give them encouraging advice about their journey ahead.
    """
    
    print("💭 Sending prompt to AI...\n")
    
    # Step 3: Invoke the AI with our prompt
    # 'await' means "wait for the response before continuing"
    response = await kernel.invoke_prompt(
        prompt=prompt,
        function_name="career_advice"
    )
    
    # Step 4: Display the response
    print("🤖 AI Response:")
    print("=" * 60)
    print(response)
    print("=" * 60)
    
    print("\n✅ First AI conversation complete!")
    print(f"💰 Approximate cost: $0.0001 (less than a penny!)")
    
    return response


# This is the entry point when we run the script
if __name__ == "__main__":
    # Run our async function
    # asyncio.run() starts the async event loop
    asyncio.run(first_ai_conversation())