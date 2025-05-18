from db_config import get_db
from datetime import datetime
from gen_summary import generate_summary
import asyncio
import traceback

async def store_conversation(message_summary):
    """
    Store the conversation in MongoDB with both raw messages and concise summary
    Args:
        message_summary: List of messages from the conversation
    """
    print("\n=== STORE_CONVERSATION CALLED ===")
    print(f"Message summary: {message_summary}")
    try:
        print("Starting conversation storage process...")
        print(f"Message summary length: {len(message_summary)}")
        
        db = get_db()
        print("Database connection successful")
        
        collection = db["messages"]
        print("Collection access successful")

        # Generate concise summary
        print("Generating concise summary...")
        concise_summary = await generate_summary(message_summary)
        print(f"Generated summary: {concise_summary}")

        # Join raw messages into a single text
        raw_messages = " ".join(message_summary)
        print(f"Raw messages length: {len(raw_messages)}")

        doc = {
            "raw_messages": raw_messages,
            "concise_summary": concise_summary,
            "created_at": datetime.utcnow()
        }
        print("Document prepared for insertion")

        result = collection.insert_one(doc)
        print(f"Conversation stored with ID: {result.inserted_id}")
        print(f"Concise Summary: {concise_summary}")
        return True
    except Exception as e:
        print(f"Error storing conversation: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        return False

# Only run this if the file is run directly
if __name__ == "__main__":
    # This is for testing the storage function directly
    test_messages = ["Test message 1", "Test message 2"]
    asyncio.run(store_conversation(test_messages))