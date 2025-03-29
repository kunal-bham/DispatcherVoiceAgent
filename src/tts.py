import httpx
import os
from .config import OPENAI_API_KEY, OPENAI_API_BASE
import soundfile as sf
import numpy as np
from scipy import signal

TTS_ENDPOINT = f"{OPENAI_API_BASE}/audio/speech"

def apply_voice_modulation(audio_data, sample_rate):
    """
    Apply subtle voice modulation to make it sound more human-like
    """
    # Add slight pitch variation
    pitch_variation = np.random.uniform(0.98, 1.02)
    audio_data = signal.resample(audio_data, int(len(audio_data) * pitch_variation))
    
    # Add subtle reverb effect
    delay = int(0.05 * sample_rate)
    decay = 0.3
    reverb = np.zeros_like(audio_data)
    reverb[delay:] = audio_data[:-delay] * decay
    audio_data = audio_data + reverb
    
    return audio_data

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
            "voice": "nova",  # Using 'nova' voice which is optimized for natural speech
            "speed": 1.0  # Natural speaking speed
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(TTS_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            
            # Save the audio file
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            # Apply voice modulation
            audio_data, sample_rate = sf.read(output_file)
            modulated_audio = apply_voice_modulation(audio_data, sample_rate)
            sf.write(output_file, modulated_audio, sample_rate)
            
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