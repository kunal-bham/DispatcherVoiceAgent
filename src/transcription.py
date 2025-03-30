import httpx
import os
from config import OPENAI_API_KEY, WHISPER_ENDPOINT
import asyncio
import traceback

async def transcribe_audio(audio_data):
    """Transcribe audio using OpenAI's Whisper API"""
    try:
        # Check if API key is set
        if not OPENAI_API_KEY:
            print("Error: OPENAI_API_KEY is not set in environment variables")
            return None

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
                "language": "en"
            }
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    print(f"Making request to: {WHISPER_ENDPOINT}")
                    response = await client.post(WHISPER_ENDPOINT, headers=headers, files=files, data=data)
                    print(f"Response status code: {response.status_code}")
                    
                    if response.status_code != 200:
                        print(f"Error response: {response.text}")
                        return None
                        
                    result = response.json()
                    transcription = result["text"]
                    print("Transcription successful")
            except asyncio.CancelledError:
                print("Transcription cancelled")
                return None
            except Exception as e:
                print(f"Error in transcription API call: {e}")
                print("Full traceback:")
                print(traceback.format_exc())
                return None
        
        # Clean up temporary file
        try:
            os.remove("temp_audio.wav")
            print("Temporary file cleaned up")
        except Exception as e:
            print(f"Error cleaning up temporary file: {e}")
            
        return transcription
    except Exception as e:
        print(f"Error in transcription: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        return None 