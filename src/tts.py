import os
from TTS.api import TTS
import soundfile as sf
import numpy as np
from scipy import signal
from alloy_config import ALLOY_CONFIG

# Initialize TTS with a high-quality model only once
# Using FastSpeech2 model which is more reliable and natural sounding
_tts = None

def get_tts():
    global _tts
    if _tts is None:
        _tts = TTS(model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False)
    return _tts

def apply_voice_modulation(audio_data, sample_rate):
    """
    Apply voice modulation using Alloy's voice settings for more sincere and natural speech
    """
    # Apply pitch variation based on Alloy settings with more natural variation
    pitch_variation = ALLOY_CONFIG["voice_settings"]["pitch"]
    # Add subtle pitch variation throughout the audio
    pitch_envelope = np.linspace(0.95, 1.05, len(audio_data))
    audio_data = signal.resample(audio_data, int(len(audio_data) * pitch_variation))
    
    # Apply energy modulation with smoother transitions
    energy = ALLOY_CONFIG["voice_settings"]["energy"]
    # Create a more natural energy envelope with slight variations
    envelope = np.linspace(0.85, 1.15, len(audio_data))
    # Add subtle random variations to the envelope
    envelope += np.random.normal(0, 0.05, len(audio_data))
    audio_data = audio_data * envelope
    
    # Add subtle reverb effect for natural sound
    delay = int(0.03 * sample_rate)  # Reduced delay for more natural sound
    decay = 0.2  # Reduced decay for subtler effect
    reverb = np.zeros_like(audio_data)
    reverb[delay:] = audio_data[:-delay] * decay
    audio_data = audio_data + reverb
    
    # Add subtle breath effect with varying intensity
    breath_intensity = np.random.uniform(0.005, 0.015)
    breath = np.random.normal(0, breath_intensity, len(audio_data))
    audio_data = audio_data + breath
    
    # Add subtle vibrato effect for more human-like quality
    vibrato_freq = 5  # Hz
    vibrato_depth = 0.02
    t = np.arange(len(audio_data)) / sample_rate
    vibrato = np.sin(2 * np.pi * vibrato_freq * t) * vibrato_depth
    audio_data = audio_data * (1 + vibrato)
    
    # Normalize audio to prevent clipping
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    return audio_data

async def text_to_speech(text: str, output_file: str = "response.mp3"):
    """
    Convert text to speech using Coqui TTS with Alloy's voice settings
    Args:
        text: The text to convert to speech
        output_file: The output file path for the audio
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get the TTS model instance
        tts = get_tts()
        
        # Generate speech with Coqui TTS
        tts.tts_to_file(
            text=text,
            file_path=output_file,
            speed=ALLOY_CONFIG["voice_settings"]["speed"],
            # Add pitch variation for more natural sound
            pitch=ALLOY_CONFIG["voice_settings"]["pitch"]
        )
        
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