import httpx
import os
from .config import OPENAI_API_KEY, OPENAI_API_BASE

TTS_ENDPOINT = f"{OPENAI_API_BASE}/audio/speech"

async def text_to_speech(text: str, output_file: str = "response.mp3"):
    """
    Convert text to speech using OpenAI's TTS API with optimized settings for natural sound
    Args:
        text: The text to convert to speech
        output_file: The output file path for the audio
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "tts-1-hd",  # Using HD model for better quality
            "input": text,
            "voice": "nova"  # Using 'nova' voice which is optimized for natural speech
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(TTS_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            
            # Save the audio file
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            return True
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")
        return False

def play_audio(file_path: str):
    """
    Play the generated audio file
    Args:
        file_path: Path to the audio file
    """
    try:
        if os.name == 'nt':  # Windows
            os.system(f'start {file_path}')
        elif os.name == 'posix':  # macOS and Linux
            os.system(f'afplay {file_path}')
    except Exception as e:
        print(f"Error playing audio: {e}") 