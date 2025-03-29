import os
import httpx
import asyncio
import time
import sys
import select
from dotenv import load_dotenv
from config import SYSTEM_PROMPT, OPENAI_API_KEY, CHAT_ENDPOINT
from alloy_config import ALLOY_CONFIG

# Load environment variables
load_dotenv()

# Initialize messages with system prompt
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

def check_for_input(timeout):
    """Check if there is input available within the timeout period"""
    start_time = time.time()
    has_input = False
    
    while time.time() - start_time < timeout:
        if select.select([sys.stdin], [], [], 0.1)[0]:
            has_input = True
            break
    return has_input

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
            # Debug: Print request data
            print(f"Debug - Request data: {data}")
            
            response = await client.post(CHAT_ENDPOINT, headers=headers, json=data)
            
            # Debug: Print response status and headers
            print(f"Debug - Response status: {response.status_code}")
            print(f"Debug - Response headers: {dict(response.headers)}")
            
            if response.status_code == 429:
                print("\nRate limit reached. Waiting 60 seconds before retrying...")
                await asyncio.sleep(60)  # Wait 60 seconds before retrying
                return await get_ai_response(transcription, messages)  # Retry the request
                
            response.raise_for_status()
            result = response.json()
            bot_message = result["choices"][0]["message"]["content"]
            
            # Apply conversation style based on context
            if not messages[-1]["role"] == "assistant":  # First response
                bot_message = ALLOY_CONFIG["conversation_style"]["greeting"] + " " + bot_message
            elif "?" in transcription:  # Question detected
                bot_message = ALLOY_CONFIG["conversation_style"]["acknowledgment"] + " " + bot_message
            
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

async def emergency_chat():
    """Main emergency chat loop with Alloy personality"""
    print("\nEmergency Assistant is ready. Type your messages below (type 'exit' to quit):\n")
    print("You: ", end='', flush=True)
    count = 0
    
    while True:       
        try:
            if check_for_input(3):
                user_input = input().strip()
                if user_input.lower() == 'exit':
                    print(ALLOY_CONFIG["conversation_style"]["closing"])
                    break
                    
                response = await get_ai_response(user_input, messages)
                if response:
                    print(f"\nAI: {response}\n")
                    print("You: ", end='', flush=True)
            elif count == 0:
                print()  # Move to next line
                response = await get_ai_response("911 what's your emergency?", messages)
                if response:
                    print(f"\nAI: {response}\n")
                    print("You: ", end='', flush=True)
                    count += 1
        except KeyboardInterrupt:
            print("\n" + ALLOY_CONFIG["conversation_style"]["closing"])
            break
        except Exception as e:
            print(f"Error: {e}\n")
            break

if __name__ == "__main__":
    asyncio.run(emergency_chat()) 