"""
Episode 2: Testing the Job Scraper Plugin

This script demonstrates:
1. How to add a plugin to the kernel
2. How to call plugin functions directly
3. How to let the kernel invoke plugin functions
"""

import asyncio
import sys
import os
import json

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.kernel_config import create_kernel
from src.plugins.job_intelligence import JobScraperPlugin


async def test_plugin_direct():
    """
    Test 1: Call plugin function directly (without kernel)
    
    This shows that plugins are just Python classes with methods.
    """
    print("=" * 60)
    print("TEST 1: Direct Plugin Call")
    print("=" * 60)
    
    # Create plugin instance
    scraper = JobScraperPlugin()
    
    # Call the function directly
    print("\n🔍 Searching for GenAI jobs...\n")
    result_json = await scraper.scrape_genai_jobs(
        keywords="GenAI,LLM,machine learning,AI engineer",
        limit=10
    )
    
    # Parse and display results
    result = json.loads(result_json)
    
    print(f"\n📊 Results:")
    print(f"Total jobs found: {result['total_jobs']}")
    print(f"Timestamp: {result['timestamp']}")
    
    print("\n📋 Sample Jobs:")
    for i, job in enumerate(result['jobs'][:3], 1):  # Show first 3
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
        print(f"   URL: {job['url']}")
    
    return result_json


async def test_plugin_with_kernel():
    """
    Test 2: Add plugin to kernel and invoke through kernel
    
    This is the "proper" way - lets the kernel manage the plugin.
    """
    print("\n" + "=" * 60)
    print("TEST 2: Plugin via Kernel")
    print("=" * 60)
    
    # Create kernel
    kernel = create_kernel()
    
    # Create plugin instance
    scraper = JobScraperPlugin()
    
    # Add plugin to kernel
    # Now the kernel "knows about" this plugin and its functions
    kernel.add_plugin(
        plugin=scraper,
        plugin_name="job_intelligence"
    )
    
    print("\n✅ Plugin added to kernel!")
    print("📦 Available functions:")
    
    # List all functions in the plugin
    for function_name in kernel.plugins["job_intelligence"]:
        func = kernel.plugins["job_intelligence"].functions[function_name]
        print(f"   - {function_name}: {func.description}")
    
    # Invoke function through kernel
    print("\n🔍 Invoking scrape_genai_jobs through kernel...\n")
    
    result = await kernel.invoke(
        function=kernel.plugins["job_intelligence"]["scrape_genai_jobs"],
        keywords="Python,AI,machine learning",
        limit=5
    )
    
    print(f"\n✅ Kernel invocation successful!")
    print(f"📊 Found {json.loads(str(result))['total_jobs']} jobs")
    
    return result


async def test_job_stats():
    """
    Test 3: Use multiple plugin functions together
    
    This demonstrates how plugins can have multiple related functions.
    """
    print("\n" + "=" * 60)
    print("TEST 3: Multiple Plugin Functions")
    print("=" * 60)
    
    scraper = JobScraperPlugin()
    
    # First, scrape jobs
    print("\n🔍 Step 1: Scraping jobs...")
    jobs_json = await scraper.scrape_genai_jobs(
        keywords="AI,GenAI,LLM",
        limit=15
    )
    
    # Then, get stats
    print("\n📊 Step 2: Analyzing jobs...")
    stats_json = await scraper.get_job_stats(jobs_json)
    
    # Display stats
    stats = json.loads(stats_json)
    print("\n📈 Job Market Statistics:")
    print(f"Total jobs analyzed: {stats['total_jobs']}")
    print(f"Unique companies: {stats['unique_companies']}")
    print(f"\nJobs by source:")
    for source, count in stats['jobs_by_source'].items():
        print(f"   {source}: {count} jobs")
    
    print(f"\nTop companies hiring:")
    for company in stats['top_companies'][:5]:
        print(f"   - {company}")


async def main():
    """
    Main test runner
    """
    print("🚀 Episode 2: Job Scraper Plugin Tests\n")
    
    try:
        # Run all tests
        await test_plugin_direct()
        await test_plugin_with_kernel()
        await test_job_stats()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n💡 Key Learnings:")
        print("1. Plugins are Python classes with @kernel_function methods")
        print("2. Functions can be called directly or through the kernel")
        print("3. Plugins can have multiple related functions")
        print("4. Native functions use regular Python code (not AI)")
        print("\n💰 Cost: $0 (using free APIs, no AI calls)")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())