import speech_recognition as sr
import asyncio
from src.config import SYSTEM_PROMPT
from src.transcription import transcribe_audio
from src.ai_handler import get_ai_response
from src.tts import text_to_speech, play_audio

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
                        
                        # Convert AI response to speech and play it
                        audio_file = "ai_response.mp3"
                        if await text_to_speech(ai_response, audio_file):
                            play_audio(audio_file)
                            # Clean up the audio file after playing
                            try:
                                os.remove(audio_file)
                            except:
                                pass
                
            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                print("\nStopping the voice agent...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(main()) 