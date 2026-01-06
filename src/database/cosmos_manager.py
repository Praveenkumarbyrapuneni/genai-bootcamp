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
            "type": "comprehensive_analysis",
            "is_deleted": False,  # New field
            "is_archived": False  # New field
        }
        
        print("Analysis Data:", analysis_data)
        
        try:
            self.container.upsert_item(document)
            print(f"✅ Saved to Cloud: {record_id}")
            return record_id
        except exceptions.CosmosHttpResponseError as e:
            print(f"❌ Azure Save Failed: {e.message}")
            return None

    def get_user_history(self, user_id: str, include_archived: bool = False):
        """
        Retrieves all past analyses for a specific user.
        Filters out deleted records by default.
        
        Args:
            user_id: User's ID
            include_archived: If False, also filters out archived records
        """
        # Build query to exclude deleted items
        if include_archived:
            query = """
                SELECT * FROM c 
                WHERE c.user_id = @user_id 
                AND (c.is_deleted = false OR NOT IS_DEFINED(c.is_deleted))
                ORDER BY c.timestamp DESC
            """
        else:
            query = """
                SELECT * FROM c 
                WHERE c.user_id = @user_id 
                AND (c.is_deleted = false OR NOT IS_DEFINED(c.is_deleted))
                AND (c.is_archived = false OR NOT IS_DEFINED(c.is_archived))
                ORDER BY c.timestamp DESC
            """
        
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
    
    def bulk_delete(self, ids: list[str], user_id: str) -> dict:
        """
        Soft delete multiple analyses (set is_deleted = true).
        Verifies ownership before deleting.
        
        Args:
            ids: List of document IDs to delete
            user_id: User ID to verify ownership
            
        Returns:
            Dict with updated count, failed count, and failed IDs
        """
        updated = 0
        failed = 0
        failed_ids = []
        
        for record_id in ids:
            try:
                # Read the item first to verify ownership
                item = self.container.read_item(item=record_id, partition_key=user_id)
                
                # Verify user owns this record
                if item.get("user_id") != user_id:
                    failed += 1
                    failed_ids.append(record_id)
                    print(f"⚠️ User {user_id} attempted to delete record {record_id} owned by {item.get('user_id')}")
                    continue
                
                # Update the record
                item["is_deleted"] = True
                item["deleted_at"] = datetime.now().isoformat()
                self.container.upsert_item(item)
                updated += 1
                print(f"✅ Soft deleted: {record_id}")
                
            except exceptions.CosmosResourceNotFoundError:
                failed += 1
                failed_ids.append(record_id)
                print(f"❌ Record not found: {record_id}")
            except Exception as e:
                failed += 1
                failed_ids.append(record_id)
                print(f"❌ Failed to delete {record_id}: {e}")
        
        return {
            "updated": updated,
            "failed": failed,
            "failed_ids": failed_ids
        }
    
    def bulk_archive(self, ids: list[str], user_id: str, is_archived: bool) -> dict:
        """
        Archive or unarchive multiple analyses.
        Verifies ownership before updating.
        
        Args:
            ids: List of document IDs to archive/unarchive
            user_id: User ID to verify ownership
            is_archived: True to archive, False to unarchive
            
        Returns:
            Dict with updated count, failed count, and failed IDs
        """
        updated = 0
        failed = 0
        failed_ids = []
        
        for record_id in ids:
            try:
                # Read the item first to verify ownership
                item = self.container.read_item(item=record_id, partition_key=user_id)
                
                # Verify user owns this record
                if item.get("user_id") != user_id:
                    failed += 1
                    failed_ids.append(record_id)
                    print(f"⚠️ User {user_id} attempted to archive record {record_id} owned by {item.get('user_id')}")
                    continue
                
                # Update the record
                item["is_archived"] = is_archived
                item["archived_at"] = datetime.now().isoformat() if is_archived else None
                self.container.upsert_item(item)
                updated += 1
                action = "archived" if is_archived else "unarchived"
                print(f"✅ {action.capitalize()}: {record_id}")
                
            except exceptions.CosmosResourceNotFoundError:
                failed += 1
                failed_ids.append(record_id)
                print(f"❌ Record not found: {record_id}")
            except Exception as e:
                failed += 1
                failed_ids.append(record_id)
                print(f"❌ Failed to archive {record_id}: {e}")
        
        return {
            "updated": updated,
            "failed": failed,
            "failed_ids": failed_ids
        }

if __name__ == "__main__":
    print("Testing Cloud Connection...")
    try:
        db = CareerDataManager()
        print("Success! Connected to Azure.")
    except Exception as e:
        print(f"Failed: {e}")