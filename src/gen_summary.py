import httpx
from config import OPENAI_API_KEY, CHAT_ENDPOINT

async def generate_summary(messages):
    """
    Generate a concise one-sentence summary of the conversation using GPT
    Args:
        messages: List of messages from the conversation
    Returns:
        str: A concise one-sentence summary of the emergency call
    """
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = (
            "Create a concise one-sentence summary of this emergency call. "
            "Focus on the type of emergency, location if mentioned, and any critical details. "
            "Make it clear and professional. Here's the conversation:\n\n"
            f"{' '.join(messages)}"
        )
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0.3  # Lower temperature for more focused output
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(CHAT_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            summary = result["choices"][0]["message"]["content"].strip()
            return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return " ".join(messages)  # Fallback to original message if summary fails
