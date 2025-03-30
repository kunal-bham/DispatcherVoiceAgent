import speech_recognition as sr
import asyncio
import time
import os
import sys
from dotenv import load_dotenv

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import SYSTEM_PROMPT
from transcription import transcribe_audio
from ai_handler import get_ai_response
from tts import text_to_speech, play_audio
from alloy_config import ALLOY_CONFIG
from store_message import store_conversation
from gen_summary import generate_summary

# Load environment variables
load_dotenv()

async def main():
    # Start overall timing
    total_start_time = time.time()
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Initialize conversation history
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    
    # Initialize exchange counter
    exchange_count = 0
    
    # Initialize message summary
    message_summary = []

    def get_summary():
        return " ".join(message_summary)
    
    print("Starting voice-based emergency assistant...")
    print("Press Ctrl+C to stop")
    
    with sr.Microphone() as source:
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait...")
        noise_start_time = time.time()
        recognizer.adjust_for_ambient_noise(source, duration=2)
        noise_time = time.time() - noise_start_time
        print(f"Noise adjustment time: {noise_time:.2f} seconds")
        print("Ready! Speak now...")
        
        # Start with initial greeting
        greeting_start_time = time.time()
        initial_greeting = ALLOY_CONFIG["conversation_style"]["greeting"]
        print(f"AI: {initial_greeting}")
        audio_file = "ai_response.mp3"
        if await text_to_speech(initial_greeting, audio_file):
            play_audio(audio_file)
            try:
                os.remove(audio_file)
            except:
                pass
        greeting_time = time.time() - greeting_start_time
        print(f"Initial greeting time: {greeting_time:.2f} seconds")
        
        while exchange_count < 2:
            try:
                # Listen for audio input with adjusted parameters
                print("\nListening...")
                listen_start_time = time.time()
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
                except sr.WaitTimeoutError:
                    print("No speech detected. Please try again.")
                    continue
                listen_time = time.time() - listen_start_time
                print(f"Listening time: {listen_time:.2f} seconds")
                
                # Start timing the entire response process
                response_start_time = time.time()
                
                # Transcribe the audio
                transcribe_start_time = time.time()
                transcription = await transcribe_audio(audio)
                transcribe_time = time.time() - transcribe_start_time
                
                if transcription:
                    print(f"\nYou said: {transcription}")
                    print(f"Transcription time: {transcribe_time:.2f} seconds")
                    
                    # Add user's message to summary
                    message_summary.append(transcription)
                    
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
                        
                        # Increment exchange count
                        exchange_count += 1
                        print(f"Exchange count: {exchange_count}")
                        
                        # Print total response time
                        response_time = time.time() - response_start_time
                        print(f"\nTotal response time: {response_time:.2f} seconds")
                        
                        # Print cumulative time
                        cumulative_time = time.time() - total_start_time
                        print(f"Cumulative time: {cumulative_time:.2f} seconds")

                        # Print message summary after each exchange
                        print("\nMessage Summary:")
                        print("---------------")
                        print(get_summary())

                        # If this was the last exchange, wait for final response
                        if exchange_count >= 2:
                            print("\nWaiting for final response...")
                            try:
                                final_audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
                                final_transcription = await transcribe_audio(final_audio)
                                if final_transcription:
                                    print(f"\nFinal response: {final_transcription}")
                                    message_summary.append(final_transcription)
                            except Exception as e:
                                print(f"Error getting final response: {e}")
                
            except KeyboardInterrupt:
                print("\n=== KEYBOARD INTERRUPT DETECTED ===")
                print("Stopping the voice agent...")
                # Print final message summary
                print("\nFinal Message Summary:")
                print("---------------------")
                print(get_summary())
                print("\nAttempting to store conversation...")
                try:
                    # Store the conversation with both raw messages and summary
                    await store_conversation(message_summary)
                    print("Storage process completed")
                except Exception as e:
                    print(f"Error during storage: {e}")
                finally:
                    # Ensure we break out of the loop
                    break
            except Exception as e:
                print(f"\n=== ERROR DETECTED ===")
                print(f"An error occurred: {e}")
                print("Attempting to store conversation...")
                # Store the conversation even if there's an error
                await store_conversation(message_summary)
                print("Storage process completed")
                continue
        
        # Print closing message when we exit the loop
        print("Transferring to hotline...")
        # Convert closing message to speech and play it
        audio_file = "ai_response.mp3"
        if await text_to_speech("A human dispatcher is now available. I'm transferring your call to them...", audio_file):
            play_audio(audio_file)
            try:
                os.remove(audio_file)
            except:
                pass

if __name__ == "__main__":
    asyncio.run(main()) 