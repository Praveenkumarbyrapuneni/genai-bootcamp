# src/database/cosmos_manager.py

import os
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from dotenv import load_dotenv
from typing import Sequence, Dict

class CareerDataManager:
    """
    Manages Long-Term Memory using Azure Cosmos DB.
    """
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv("COSMOS_CONNECTION_STRING")
        
        if not self.connection_string:
            raise ValueError("❌ Missing COSMOS_CONNECTION_STRING in .env file")

        try:
            # Initialize Client
            self.client = CosmosClient.from_connection_string(self.connection_string)
            
            # Connect to Database
            self.database_name = "careerpath_db"
            self.database = self.client.create_database_if_not_exists(id=self.database_name)
            
            # Connect to Container (think of this as a Table)
            self.container_name = "analysis_history"
            self.container = self.database.create_container_if_not_exists(
                id=self.container_name,
                partition_key=PartitionKey(path="/user_id"),
                offer_throughput=400 # Minimum throughput
            )
            print(f"☁️ Connected to Azure Cosmos DB: {self.database_name}")
            
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            raise e

    def save_career_analysis(self, user_id: str, role: str, analysis_data: dict):
        """
        Saves a full career analysis report to the cloud.
        """
        record_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Prepare the document (Must be JSON serializable)
        document = {
            "id": record_id,
            "user_id": user_id,
            "target_role": role,
            "timestamp": timestamp,
            "data": analysis_data,
            "type": "comprehensive_analysis"
        }
        
        print("Analysis Data:", analysis_data)
        
        try:
            self.container.upsert_item(document)
            print(f"✅ Saved to Cloud: {record_id}")
            return record_id
        except exceptions.CosmosHttpResponseError as e:
            print(f"❌ Azure Save Failed: {e.message}")
            return None

    def get_user_history(self, user_id: str):
        """
        Retrieves all past analyses for a specific user.
        """
        query = "SELECT * FROM c WHERE c.user_id = @user_id ORDER BY c.timestamp DESC"
        parameters: Sequence[Dict[str, object]] = [{"name": "@user_id", "value": user_id}]
        
        try:
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=False
            ))
            return items
        except exceptions.CosmosHttpResponseError as e:
            print(f"❌ Azure Read Failed: {e.message}")
            return []

if __name__ == "__main__":
    print("Testing Cloud Connection...")
    try:
        db = CareerDataManager()
        print("Success! Connected to Azure.")
    except Exception as e:
        print(f"Failed: {e}")