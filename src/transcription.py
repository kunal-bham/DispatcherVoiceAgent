import httpx
import os
from config import OPENAI_API_KEY, WHISPER_ENDPOINT
import asyncio
import traceback
import tempfile

async def transcribe_audio(audio_data):
    """Transcribe audio using OpenAI's Whisper API and detect language"""
    try:
        # Check if API key is set
        if not OPENAI_API_KEY:
            print("Error: OPENAI_API_KEY is not set in environment variables")
            return None, None

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Save audio data to temporary file
        print("Saving audio data to temporary file...")
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data.get_wav_data())
        
        # Check file size
        file_size = os.path.getsize("temp_audio.wav")
        print(f"Audio file size: {file_size} bytes")
        
        # Send request to Whisper API
        print("Sending request to Whisper API...")
        with open("temp_audio.wav", "rb") as f:
            files = {"file": ("audio.wav", f, "audio/wav")}
            data = {
                "model": "whisper-1",
                "response_format": "json",
                "language": None  # Let Whisper auto-detect the language
            }
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    print(f"Making request to: {WHISPER_ENDPOINT}")
                    response = await client.post(WHISPER_ENDPOINT, headers=headers, files=files, data=data)
                    print(f"Response status code: {response.status_code}")
                    
                    if response.status_code != 200:
                        print(f"Error response: {response.text}")
                        return None, None
                        
                    result = response.json()
                    transcription = result["text"]
                    detected_language = result.get("language", "en")  # Default to English if not detected
                    print(f"Transcription successful. Detected language: {detected_language}")
            except asyncio.CancelledError:
                print("Transcription cancelled")
                return None, None
            except Exception as e:
                print(f"Error in transcription API call: {e}")
                print("Full traceback:")
                print(traceback.format_exc())
                return None, None
        
        # Clean up temporary file
        try:
            os.remove("temp_audio.wav")
            print("Temporary file cleaned up")
        except Exception as e:
            print(f"Error cleaning up temporary file: {e}")
            
        return transcription, detected_language
    except Exception as e:
        print(f"Error in transcription: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        return None, None 