import httpx
from .config import OPENAI_API_KEY, CHAT_ENDPOINT

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
        "temperature": 0.3
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(CHAT_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            bot_message = result["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": bot_message})
            return bot_message
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return None 