import speech_recognition as sr
import asyncio
import time
from src.config import SYSTEM_PROMPT
from src.transcription import transcribe_audio
from src.ai_handler import get_ai_response
from src.tts import text_to_speech, play_audio
from src.alloy_config import ALLOY_CONFIG

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
        
        # Start with initial greeting
        initial_greeting = ALLOY_CONFIG["conversation_style"]["greeting"]
        print(f"AI: {initial_greeting}")
        audio_file = "ai_response.mp3"
        if await text_to_speech(initial_greeting, audio_file):
            play_audio(audio_file)
            try:
                os.remove(audio_file)
            except:
                pass
        
        while True:
            try:
                # Listen for audio input with adjusted parameters
                print("\nListening...")
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
                except sr.WaitTimeoutError:
                    print("No speech detected. Please try again.")
                    continue
                
                # Start timing the entire response process
                total_start_time = time.time()
                
                # Transcribe the audio
                transcribe_start_time = time.time()
                transcription = await transcribe_audio(audio)
                transcribe_time = time.time() - transcribe_start_time
                
                if transcription:
                    print(f"\nYou said: {transcription}")
                    print(f"Transcription time: {transcribe_time:.2f} seconds")
                    
                    # Get AI response
                    ai_start_time = time.time()
                    ai_response = await get_ai_response(transcription, messages)
                    ai_time = time.time() - ai_start_time
                    
                    if ai_response:
                        print(f"AI: {ai_response}")
                        print(f"AI response time: {ai_time:.2f} seconds")
                        
                        # Convert AI response to speech and play it
                        tts_start_time = time.time()
                        audio_file = "ai_response.mp3"
                        if await text_to_speech(ai_response, audio_file):
                            play_audio(audio_file)
                            # Clean up the audio file after playing
                            try:
                                os.remove(audio_file)
                            except:
                                pass
                        tts_time = time.time() - tts_start_time
                        print(f"TTS processing time: {tts_time:.2f} seconds")
                        
                        # Print total time
                        total_time = time.time() - total_start_time
                        print(f"\nTotal response time: {total_time:.2f} seconds")
                
            except KeyboardInterrupt:
                print("\nStopping the voice agent...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(main()) 