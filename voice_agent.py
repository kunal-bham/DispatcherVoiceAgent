import speech_recognition as sr
import os
import json
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = "https://api.openai.com/v1"
WHISPER_ENDPOINT = f"{OPENAI_API_BASE}/audio/transcriptions"
CHAT_ENDPOINT = f"{OPENAI_API_BASE}/chat/completions"

SYSTEM_PROMPT = (
    "You are a calm, assertive emergency AI assistant. "
    "Gather critical details quickly and respond clearly. "
    "Prioritize life-threatening emergencies. Ask for location, nature of emergency, and if help is needed."
)

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
                "model": "whisper-1"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    WHISPER_ENDPOINT,
                    headers=headers,
                    files=files,
                    data=data
                )
                response.raise_for_status()
                result = response.json()
                return result["text"]
    finally:
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")

async def get_ai_response(transcription, messages):
    """Get AI response using GPT-4 via httpx"""
    messages.append({"role": "user", "content": transcription})
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4-0613",
        "messages": messages,
        "temperature": 0.3
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(CHAT_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            bot_message = result["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": bot_message})
            return bot_message
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return None

async def main():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Initialize conversation history
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    
    print("Starting voice-based emergency assistant...")
    print("Press Ctrl+C to stop")
    
    with sr.Microphone() as source:
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Ready! Speak now...")
        
        while True:
            try:
                # Listen for audio input
                print("\nListening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Transcribe the audio
                transcription = await transcribe_audio(audio)
                if transcription:
                    print(f"\nYou said: {transcription}")
                    
                    # Get AI response
                    ai_response = await get_ai_response(transcription, messages)
                    if ai_response:
                        print(f"AI: {ai_response}")
                
            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                print("\nStopping the voice agent...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 