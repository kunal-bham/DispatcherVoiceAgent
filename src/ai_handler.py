import httpx
from .config import OPENAI_API_KEY, CHAT_ENDPOINT, SYSTEM_PROMPT
import time
import sys
import select

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
    """Get AI response using GPT-4 via httpx"""
    messages.append({"role": "user", "content": transcription})
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4-0613",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 150,  # Limit response length for faster processing
        "presence_penalty": 0.0,  # Reduce presence penalty for faster responses
        "frequency_penalty": 0.0,  # Reduce frequency penalty for faster responses
        "stream": False  # Disable streaming for faster complete response
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:  # Set explicit timeout
            response = await client.post(CHAT_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            bot_message = result["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": bot_message})
            return bot_message
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return None

async def emergency_chat():
    """Main emergency chat loop"""
    print("\nEmergency Assistant is ready. Type your messages below (type 'exit' to quit):\n")
    print("You: ", end='', flush=True)
    count = 0
    
    while True:       
        try:
            if check_for_input(3):
                user_input = input().strip()
                if user_input.lower() == 'exit':
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
            break
        except Exception as e:
            print(f"Error: {e}\n")
            break 