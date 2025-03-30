import httpx
from .config import OPENAI_API_KEY, CHAT_ENDPOINT, SYSTEM_PROMPT
from .alloy_config import ALLOY_CONFIG
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
    """Get AI response using GPT-4 via httpx with Alloy configuration"""
    api_start_time = time.time()
    messages.append({"role": "user", "content": transcription})
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Apply Alloy configuration settings
    data = {
        "model": "gpt-4-0613",
        "messages": messages,
        **ALLOY_CONFIG["response_settings"]
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            request_start_time = time.time()
            response = await client.post(CHAT_ENDPOINT, headers=headers, json=data)
            request_time = time.time() - request_start_time
            print(f"API request time: {request_time:.2f} seconds")
            
            response.raise_for_status()
            result = response.json()
            bot_message = result["choices"][0]["message"]["content"]
            
            # Only add acknowledgment for questions, not greetings
            if "?" in transcription and not messages[-2]["role"] == "assistant":
                bot_message = ALLOY_CONFIG["conversation_style"]["acknowledgment"] + " " + bot_message
            
            messages.append({"role": "assistant", "content": bot_message})
            total_api_time = time.time() - api_start_time
            print(f"Total API processing time: {total_api_time:.2f} seconds")
            return bot_message
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return None

async def emergency_chat():
    """Main emergency chat loop with Alloy personality"""
    total_start_time = time.time()
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
    
    total_time = time.time() - total_start_time
    print(f"\nTotal conversation time: {total_time:.2f} seconds") 