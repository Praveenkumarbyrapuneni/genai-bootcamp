# episodes/ep08_persistence/test_db.py

import sys
import os
import time

# Add the src directory to Python's path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.database.cosmos_manager import CareerDataManager

def test_local_persistence():
    print("\n🎬 Episode 8: Testing Local Storage Bypass")
    print("=" * 50)

    # 1. Initialize Manager
    db_manager = CareerDataManager()

    # 2. Simulate Data (Mocking what the Agents would produce)
    mock_user_id = "test_user_local"
    mock_role = "Senior GenAI Engineer"
    mock_analysis_data = {
        "market_outlook": "Very High Demand",
        "missing_skills": ["Cosmos DB", "Semantic Kernel"],
        "strategy": "Build a portfolio project",
        "readiness_score": 85
    }

    print(f"\n📝 Saving mock analysis for {mock_user_id}...")
    
    # 3. Save Data
    record_id = db_manager.save_career_analysis(
        user_id=mock_user_id,
        role=mock_role,
        analysis_data=mock_analysis_data
    )

    print(f"✅ Record saved with ID: {record_id}")
    print("⏳ Reading back data...")

    # 4. Read Data Back
    history = db_manager.get_user_history(mock_user_id)
    
    if len(history) > 0:
        latest = history[0]
        print("\n✅ SUCCESS! Retrieved saved data:")
        print(f"   Role: {latest['target_role']}")
        print(f"   Score: {latest['data']['readiness_score']}")
        print(f"   Stored at: {latest['timestamp']}")
    else:
        print("❌ Failed to retrieve data.")

if __name__ == "__main__":
    test_local_persistence()