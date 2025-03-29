import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = "https://api.openai.com/v1"
WHISPER_ENDPOINT = f"{OPENAI_API_BASE}/audio/transcriptions"
CHAT_ENDPOINT = f"{OPENAI_API_BASE}/chat/completions"

SYSTEM_PROMPT = (
    "You are a calm, assertive emergency AI assistant. "
    "Gather critical details quickly and respond clearly. "
    "Prioritize life-threatening emergencies. Ask for location, nature of emergency, and if help is needed."
) 