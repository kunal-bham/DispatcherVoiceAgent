import httpx
import os
from .config import OPENAI_API_KEY, OPENAI_API_BASE
from .alloy_config import ALLOY_CONFIG
import soundfile as sf
import numpy as np
from scipy import signal

TTS_ENDPOINT = f"{OPENAI_API_BASE}/audio/speech"

def apply_voice_modulation(audio_data, sample_rate):
    """
    Apply voice modulation using Alloy's voice settings for more sincere and natural speech
    """
    # Apply pitch variation based on Alloy settings
    pitch_variation = ALLOY_CONFIG["voice_settings"]["pitch"]
    audio_data = signal.resample(audio_data, int(len(audio_data) * pitch_variation))
    
    # Apply energy modulation
    energy = ALLOY_CONFIG["voice_settings"]["energy"]
    audio_data = audio_data * energy
    
    # Add subtle reverb effect for natural sound
    delay = int(0.05 * sample_rate)
    decay = 0.3
    reverb = np.zeros_like(audio_data)
    reverb[delay:] = audio_data[:-delay] * decay
    audio_data = audio_data + reverb
    
    return audio_data

async def text_to_speech(text: str, output_file: str = "response.mp3"):
    """
    Convert text to speech using OpenAI's TTS API with Alloy's voice settings
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
        
        # Apply Alloy's voice settings
        data = {
            "model": "tts-1-hd",
            "input": text,
            "voice": "nova",
            "speed": ALLOY_CONFIG["voice_settings"]["speed"]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(TTS_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
     
            # Save the audio file
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            # Apply voice modulation with Alloy settings
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
            os.system(f'start /min wmplayer {file_path}')
        elif os.name == 'posix':  # macOS and Linux
            os.system(f'afplay {file_path}')
    except Exception as e:
        print(f"Error playing audio: {e}") 