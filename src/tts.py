import os
from TTS.api import TTS
import soundfile as sf
import numpy as np
from scipy import signal
from alloy_config import ALLOY_CONFIG

# Initialize TTS with a high-quality model only once
# Using FastSpeech2 model which is more reliable and natural sounding
_tts = None

def get_tts(language="en"):
    global _tts
    if _tts is None:
        try:
            print(f"Initializing TTS model for language: {language}")
            # Map languages to their corresponding TTS models
            model_map = {
                "en": "tts_models/en/ljspeech/fast_pitch",
                "es": "tts_models/es/css10/vits",
                "fr": "tts_models/fr/css10/vits",
                "de": "tts_models/de/thorsten/vits",
                "it": "tts_models/it/mai/tacotron2-DDC",
                "pt": "tts_models/pt/cv/vits",
                "pl": "tts_models/pl/mai/tacotron2-DDC",
                "ru": "tts_models/ru/multi_dataset/vits",
                "nl": "tts_models/nl/mai/tacotron2-DDC",
                "ar": "tts_models/ar/cv/vits",
                "ko": "tts_models/ko/kss/vits",
                "ja": "tts_models/ja/kokoro/tacotron2-DDC",
                "zh": "tts_models/zh-CN/baker/tacotron2-DDC"
            }
            
            # Get the appropriate model for the language, default to English if not supported
            model_name = model_map.get(language, "tts_models/en/ljspeech/fast_pitch")
            _tts = TTS(model_name=model_name, progress_bar=True)
            print(f"TTS model initialized successfully for {language}")
        except Exception as e:
            print(f"Error initializing TTS model: {e}")
            # Try alternative model if the first one fails
            try:
                print("Trying alternative model...")
                _tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True)
                print("Alternative TTS model initialized successfully")
            except Exception as e2:
                print(f"Error initializing alternative TTS model: {e2}")
                raise
    return _tts

def apply_voice_modulation(audio_data, sample_rate):
    """
    Apply voice modulation using Alloy's voice settings for more sincere and natural speech
    """
    # Apply pitch variation based on Alloy settings with more natural variation
    pitch_variation = ALLOY_CONFIG["voice_settings"]["pitch"]
    # Add very subtle pitch variation throughout the audio
    pitch_envelope = np.linspace(0.98, 1.02, len(audio_data))  # Reduced variation
    audio_data = signal.resample(audio_data, int(len(audio_data) * pitch_variation))
    
    # Apply energy modulation with smoother transitions
    energy = ALLOY_CONFIG["voice_settings"]["energy"]
    # Create a more stable energy envelope with minimal variations
    envelope = np.linspace(0.95, 1.05, len(audio_data))  # Reduced variation
    # Add very subtle random variations to the envelope
    envelope += np.random.normal(0, 0.02, len(audio_data))  # Reduced random variation
    audio_data = audio_data * envelope
    
    # Add very subtle reverb effect for natural sound
    delay = int(0.01 * sample_rate)  # Reduced delay
    decay = 0.1  # Reduced decay
    reverb = np.zeros_like(audio_data)
    reverb[delay:] = audio_data[:-delay] * decay
    audio_data = audio_data + reverb
    
    # Add very subtle breath effect
    breath_intensity = np.random.uniform(0.001, 0.005)  # Reduced intensity
    breath = np.random.normal(0, breath_intensity, len(audio_data))
    audio_data = audio_data + breath
    
    # Add very subtle vibrato effect
    vibrato_freq = 5  # Hz
    vibrato_depth = 0.01  # Reduced depth
    t = np.arange(len(audio_data)) / sample_rate
    vibrato = np.sin(2 * np.pi * vibrato_freq * t) * vibrato_depth
    audio_data = audio_data * (1 + vibrato)
    
    # Normalize audio to prevent clipping
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    return audio_data

async def text_to_speech(text: str, output_file: str = "response.mp3", language: str = "en"):
    """
    Convert text to speech using Coqui TTS with Alloy's voice settings
    Args:
        text: The text to convert to speech
        output_file: The output file path for the audio
        language: The language code (e.g., 'en', 'es', 'fr', etc.)
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get the TTS model instance for the specified language
        tts = get_tts(language)
        
        # Generate speech with Coqui TTS
        tts.tts_to_file(
            text=text,
            file_path=output_file,
            speed=ALLOY_CONFIG["voice_settings"]["speed"],
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