from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"Using API key (first 8 chars): {api_key[:8]}...")

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": "Say hello!"}]
    )
    print("API test successful!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"API Error: {str(e)}") 