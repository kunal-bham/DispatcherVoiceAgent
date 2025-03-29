import os
import httpx
from .config import OPENAI_API_KEY, WHISPER_ENDPOINT

async def transcribe_audio(audio_data):
    """Transcribe audio using OpenAI's Whisper model via httpx"""
    try:
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data.get_wav_data())
        
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        with open("temp_audio.wav", "rb") as f:
            files = {
                "file": ("audio.wav", f, "audio/wav")
            }
            data = {
                "model": "whisper-1",
                "response_format": "text",
                "language": "en",
                "temperature": 0.0
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    WHISPER_ENDPOINT,
                    headers=headers,
                    files=files,
                    data=data
                )
                response.raise_for_status()
                return response.text.strip()
    finally:
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav") 