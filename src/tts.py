import os
from TTS.api import TTS
import soundfile as sf
import numpy as np
from scipy import signal
from alloy_config import ALLOY_CONFIG
import unicodedata
import traceback

# Initialize TTS with a high-quality model only once
# Using FastSpeech2 model which is more reliable and natural sounding
_tts = None
_current_language = None

def preprocess_text(text: str) -> str:
    """
    Preprocess text to handle special characters and normalize unicode
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKC', text)
    print(f"Preprocessed text: {text}")
    return text

def get_tts(language="en"):
    global _tts, _current_language
    
    # Only reinitialize if language changes
    if _tts is None or _current_language != language:
        try:
            print(f"\n=== INITIALIZING TTS MODEL ===")
            print(f"Language requested: {language}")
            
            # Map languages to their corresponding TTS models
            model_map = {
                "en": "tts_models/en/ljspeech/fast_pitch",
                "es": "tts_models/es/css10/vits",  # Changed to a higher quality Spanish model
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
            print(f"Selected model: {model_name}")
            
            print("Creating TTS instance...")
            _tts = TTS(model_name=model_name, progress_bar=True)
            _current_language = language
            print(f"TTS model initialized successfully for {language}")
            
            # Print model information for debugging
            print("\nModel Information:")
            print(f"Model name: {_tts.model_name}")
            print(f"Model path: {_tts.model_path}")
            print(f"Config path: {_tts.config_path}")
            
        except Exception as e:
            print(f"\n=== ERROR INITIALIZING TTS MODEL ===")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nFull traceback:")
            print(traceback.format_exc())
            
            # Try alternative model if the first one fails
            try:
                print("\n=== TRYING ALTERNATIVE MODEL ===")
                print("Attempting to use English model as fallback...")
                _tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True)
                _current_language = "en"  # Fallback to English
                print("Alternative TTS model initialized successfully")
            except Exception as e2:
                print(f"\n=== ERROR WITH ALTERNATIVE MODEL ===")
                print(f"Error type: {type(e2).__name__}")
                print(f"Error message: {str(e2)}")
                print("\nFull traceback:")
                print(traceback.format_exc())
                raise
    return _tts

def apply_voice_modulation(audio_data, sample_rate):
    """
    Apply voice modulation using Alloy's voice settings for more sincere and natural speech
    """
    try:
        print("\n=== APPLYING VOICE MODULATION ===")
        print(f"Audio data shape: {audio_data.shape}")
        print(f"Sample rate: {sample_rate}")
        
        # Apply pitch variation based on Alloy settings with more natural variation
        pitch_variation = ALLOY_CONFIG["voice_settings"]["pitch"]
        print(f"Pitch variation: {pitch_variation}")
        
        # Add very subtle pitch variation throughout the audio
        pitch_envelope = np.linspace(0.98, 1.02, len(audio_data))  # Reduced variation
        audio_data = signal.resample(audio_data, int(len(audio_data) * pitch_variation))
        
        # Apply energy modulation with smoother transitions
        energy = ALLOY_CONFIG["voice_settings"]["energy"]
        print(f"Energy setting: {energy}")
        
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
        
        print("Voice modulation completed successfully")
        return audio_data
    except Exception as e:
        print(f"\n=== ERROR IN VOICE MODULATION ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())
        return audio_data  # Return unmodified audio if modulation fails

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
        print(f"\n=== STARTING TEXT TO SPEECH ===")
        print(f"Input text: {text}")
        print(f"Language: {language}")
        print(f"Output file: {output_file}")
        
        # Preprocess the text to handle special characters
        processed_text = preprocess_text(text)
        
        # Get the TTS model instance for the specified language
        tts = get_tts(language)
        
        # Generate speech with Coqui TTS
        print("\nGenerating speech...")
        tts.tts_to_file(
            text=processed_text,
            file_path=output_file,
            speed=ALLOY_CONFIG["voice_settings"]["speed"],
            pitch=ALLOY_CONFIG["voice_settings"]["pitch"]
        )
        
        # Verify file was created
        if not os.path.exists(output_file):
            print(f"Error: Output file {output_file} was not created")
            return False
            
        # Check file size
        file_size = os.path.getsize(output_file)
        print(f"Generated audio file size: {file_size} bytes")
        
        if file_size == 0:
            print("Error: Generated audio file is empty")
            return False
        
        # Apply voice modulation with Alloy settings
        print("\nReading generated audio file...")
        audio_data, sample_rate = sf.read(output_file)
        print(f"Audio data shape: {audio_data.shape}")
        print(f"Sample rate: {sample_rate}")
        
        # Convert stereo to mono if needed
        if len(audio_data.shape) > 1:
            print("Converting stereo to mono...")
            audio_data = np.mean(audio_data, axis=1)
        
        modulated_audio = apply_voice_modulation(audio_data, sample_rate)
        print("\nWriting modulated audio...")
        sf.write(output_file, modulated_audio, sample_rate)
        
        print("Text to speech completed successfully")
        return True
    except Exception as e:
        print(f"\n=== ERROR IN TEXT TO SPEECH ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Original text: {text}")
        print(f"Processed text: {processed_text}")
        print("\nFull traceback:")
        print(traceback.format_exc())
        return False

def play_audio(file_path: str):
    """
    Play the generated audio file
    Args:
        file_path: Path to the audio file
    """
    try:
        print(f"\n=== PLAYING AUDIO ===")
        print(f"File path: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"Error: Audio file {file_path} does not exist")
            return
            
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")
        
        if file_size == 0:
            print(f"Error: Audio file {file_path} is empty")
            return
            
        if os.name == 'nt':  # Windows
            os.system(f'start /min wmplayer {file_path}')
        elif os.name == 'posix':  # macOS and Linux
            os.system(f'afplay {file_path}')
            
        print("Audio playback completed")
    except Exception as e:
        print(f"\n=== ERROR PLAYING AUDIO ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc()) 