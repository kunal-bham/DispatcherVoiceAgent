import os
import httpx
import asyncio
from dotenv import load_dotenv
from config import SYSTEM_PROMPT, OPENAI_API_KEY, CHAT_ENDPOINT
from alloy_config import ALLOY_CONFIG

# Load environment variables
load_dotenv()

# Initialize messages with system prompt
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

async def get_ai_response(transcription, messages):
    """Get AI response using GPT-3.5-turbo via httpx with Alloy configuration"""
    # Create a copy of messages to avoid modifying the original
    current_messages = messages.copy()
    current_messages.append({"role": "user", "content": transcription})
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Simplified request data with minimal parameters
    data = {
        "model": "gpt-3.5-turbo",
        "messages": current_messages,
        "max_tokens": 100,  # Reduced from 150
        "temperature": 0.7
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(CHAT_ENDPOINT, headers=headers, json=data)
            
            if response.status_code == 429:
                print("\nRate limit reached. Waiting 60 seconds before retrying...")
                await asyncio.sleep(60)  # Wait 60 seconds before retrying
                return await get_ai_response(transcription, messages)  # Retry the request
                
            response.raise_for_status()
            result = response.json()
            bot_message = result["choices"][0]["message"]["content"]
            
            # Remove any instances of the greeting from the response
            bot_message = bot_message.replace("911, what's your emergency?", "").strip()
            bot_message = bot_message.replace("9-1-1, what's your emergency?", "").strip()
            
            # Remove any instances of the acknowledgment phrase
            bot_message = bot_message.replace(ALLOY_CONFIG["conversation_style"]["acknowledgment"], "").strip()
            
            # Only append to messages if the request was successful
            messages.append({"role": "assistant", "content": bot_message})
            return bot_message
    except httpx.HTTPError as e:
        print(f"\nError getting AI response: {e}")
        if "429" in str(e):
            print("Rate limit reached. Waiting 60 seconds before retrying...")
            await asyncio.sleep(60)  # Wait 60 seconds before retrying
            return await get_ai_response(transcription, messages)  # Retry the request
        return None
    except Exception as e:
        print(f"\nError getting AI response: {e}")
        return None 