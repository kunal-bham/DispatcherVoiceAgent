from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = 'dispatcher_db'
COLLECTION_NAME = 'messages'

def get_db():
    """Get a connection to the MongoDB database"""
    try:
        print("Attempting to connect to MongoDB...")
        client = MongoClient(MONGODB_URI)
        # Test the connection
        client.server_info()
        print("MongoDB connection successful")
        db = client[DB_NAME]
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        raise

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[DB_NAME]
            self.collection = self.db[COLLECTION_NAME]
            print("Connected to MongoDB successfully")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def store_message(self, message, message_type="emergency", metadata=None):
        """Store a message in MongoDB"""
        if not self.collection:
            self.connect()
        
        document = {
            "message": message,
            "type": message_type,
            "timestamp": datetime.utcnow(),
            "metadata": metadata or {}
        }
        
        try:
            result = self.collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            print(f"Error storing message: {e}")
            raise

    def gen_summary(self, time_range_hours=24):
        """Generate a summary of emergency calls within the specified time range"""
        if not self.collection:
            self.connect()
        
        cutoff_time = datetime.utcnow() - timedelta(hours=time_range_hours)
        
        try:
            # Get all emergency calls within the time range
            calls = self.collection.find({
                "timestamp": {"$gte": cutoff_time},
                "type": "emergency"
            })
            
            # Count total calls
            total_calls = self.collection.count_documents({
                "timestamp": {"$gte": cutoff_time},
                "type": "emergency"
            })
            
            # Group by type and count
            type_counts = self.collection.aggregate([
                {
                    "$match": {
                        "timestamp": {"$gte": cutoff_time},
                        "type": "emergency"
                    }
                },
                {
                    "$group": {
                        "_id": "$metadata.emergency_type",
                        "count": {"$sum": 1}
                    }
                }
            ])
            
            return {
                "total_calls": total_calls,
                "type_breakdown": list(type_counts),
                "time_range": f"Last {time_range_hours} hours"
            }
        except Exception as e:
            print(f"Error generating summary: {e}")
            raise

    def close(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

# Create a singleton instance
db_manager = DatabaseManager()
