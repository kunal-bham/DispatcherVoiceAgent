import traceback

def get_db():
    try:
        print("Attempting to connect to MongoDB...")
        client = MongoClient("mongodb://localhost:27017/")
        # Test the connection
        client.server_info()
        print("MongoDB connection successful")
        db = client["CALL_SUMMARY"]
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        raise