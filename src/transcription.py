import httpx
import os
from config import OPENAI_API_KEY, WHISPER_ENDPOINT
import asyncio

async def transcribe_audio(audio_data):
    """Transcribe audio using OpenAI's Whisper API"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Save audio data to temporary file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data.get_wav_data())
        
        # Send request to Whisper API
        with open("temp_audio.wav", "rb") as f:
            files = {"file": ("audio.wav", f, "audio/wav")}
            data = {
                "model": "whisper-1",
                "response_format": "json",
                "language": "en"
            }
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(WHISPER_ENDPOINT, headers=headers, files=files, data=data)
                    response.raise_for_status()
                    result = response.json()
                    transcription = result["text"]
            except asyncio.CancelledError:
                print("Transcription cancelled")
                return None
            except Exception as e:
                print(f"Error in transcription: {e}")
                return None
        
        # Clean up temporary file
        try:
            os.remove("temp_audio.wav")
        except:
            pass
            
        return transcription
    except Exception as e:
        print(f"Error in transcription: {e}")
        return None 