from openai import OpenAI
import os
from dotenv import load_dotenv
import time
import sys
import select

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")                    
client = OpenAI(api_key=api_key)


SYSTEM_PROMPT = (
    "You are a calm, assertive emergency AI assistant. "
    "Gather critical details quickly and respond clearly. "
    "Prioritize life-threatening emergencies. Ask for location, nature of emergency, and if help is needed."
)

messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

def generate_question():
    try:
        response = client.chat.completions.create(model="gpt-4-0613",
        messages=messages,
        temperature=0.3)
        bot_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_message})
        print(f"\nAI: {bot_message}\n")
        print("You: ", end='', flush=True)
    except Exception as e:
        print(f"Error: {e}\n")

def check_for_input(timeout):
    start_time = time.time()
    has_input = False
    
    while time.time() - start_time < timeout:
        if select.select([sys.stdin], [], [], 0.1)[0]:
            has_input = True
            break
    return has_input
    
def emergency_chat():
    print("\nEmergency Assistant is ready. Type your messages below (type 'exit' to quit):\n")
    print("You: ", end='', flush=True)
    count = 0
    
    while True:       
        try:
            if check_for_input(3):
                user_input = input().strip()
                if user_input.lower() == 'exit':
                    break
                    
                messages.append({"role": "user", "content": user_input})
                generate_question()
            elif count == 0:
                print()  # Move to next line
                messages.append({"role": "user", "content": "911 what's your emergency?"})
                print("\nAI: 911 what's your emergency? \n")
                print("You: ", end='', flush=True)
                count += 1
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}\n")
            break


if __name__ == "__main__":
    emergency_chat()
