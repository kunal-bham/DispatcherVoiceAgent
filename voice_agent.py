import speech_recognition as sr
import asyncio
import time
import os
import sys
from dotenv import load_dotenv
import traceback

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
    
    print("\n=== VOICE AGENT STARTED ===")
    print("Starting voice-based emergency assistant...")
    print("Press Ctrl+C to stop")
    
    with sr.Microphone() as source:
        # Adjust for ambient noise
        print("\n=== NOISE ADJUSTMENT ===")
        print("Adjusting for ambient noise... Please wait...")
        noise_start_time = time.time()
        recognizer.adjust_for_ambient_noise(source, duration=2)
        noise_time = time.time() - noise_start_time
        print(f"Noise adjustment time: {noise_time:.2f} seconds")
        print("Ready! Speak now...")
        
        # Start with initial greeting
        print("\n=== INITIAL GREETING ===")
        greeting_start_time = time.time()
        initial_greeting = ALLOY_CONFIG["conversation_style"]["greeting"]
        print(f"AI: {initial_greeting}")
        message_summary.append(initial_greeting)
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
                print("\n=== LISTENING FOR INPUT ===")
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
                print("\n=== TRANSCRIBING AUDIO ===")
                transcribe_start_time = time.time()
                transcription = await transcribe_audio(audio)
                transcribe_time = time.time() - transcribe_start_time
                
                if transcription:
                    print(f"\nYou said: {transcription}")
                    print(f"Transcription time: {transcribe_time:.2f} seconds")
                    
                    # Add user's message to summary
                    message_summary.append(transcription)
                    print(f"Message summary length: {len(message_summary)}")
                    
                    # Get AI response
                    print("\n=== GETTING AI RESPONSE ===")
                    ai_start_time = time.time()
                    ai_response = await get_ai_response(transcription, messages)
                    ai_time = time.time() - ai_start_time
                    
                    if ai_response:
                        print(f"AI: {ai_response}")
                        message_summary.append(ai_response)
                        print(f"AI response time: {ai_time:.2f} seconds")
                        
                        # Convert AI response to speech and play it
                        print("\n=== TEXT TO SPEECH ===")
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
                        print(f"\nExchange count: {exchange_count}")
                        
                        # Print total response time
                        response_time = time.time() - response_start_time
                        print(f"\nTotal response time: {response_time:.2f} seconds")
                        
                        # Print cumulative time
                        cumulative_time = time.time() - total_start_time
                        print(f"Cumulative time: {cumulative_time:.2f} seconds")

                        # Print message summary after each exchange
                        print("\n=== MESSAGE SUMMARY ===")
                        print("---------------------")
                        print(get_summary())

                        # If this was the last exchange, wait for final response
                        if exchange_count >= 1:
                            print("\n=== WAITING FOR FINAL RESPONSE ===")
                            try:
                                final_audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
                                final_transcription = await transcribe_audio(final_audio)
                                if final_transcription:
                                    print(f"\nFinal response: {final_transcription}")
                                    message_summary.append(final_transcription)
                                    
                                    # Store conversation in MongoDB after final response
                                    print("\n=== STORING CONVERSATION IN MONGODB ===")
                                    print("Message summary to store:", message_summary)
                                    try:
                                        storage_start_time = time.time()
                                        storage_result = await store_conversation(message_summary)
                                        storage_time = time.time() - storage_start_time
                                        
                                        if storage_result:
                                            print(f"Conversation stored successfully in {storage_time:.2f} seconds")
                                        else:
                                            print("Failed to store conversation")
                                            
                                    except Exception as e:
                                        print(f"Error storing conversation: {e}")
                                        print("Full traceback:")
                                        print(traceback.format_exc())
                                    
                                    # Break out of the loop after storing
                                    break
                            except Exception as e:
                                print(f"Error getting final response: {e}")
                                print("Full traceback:")
                                print(traceback.format_exc())
                                # Try to store conversation even if final response fails
                                try:
                                    print("\nAttempting to store conversation after error...")
                                    storage_result = await store_conversation(message_summary)
                                    if storage_result:
                                        print("Conversation stored successfully after error")
                                    else:
                                        print("Failed to store conversation after error")
                                except Exception as store_error:
                                    print(f"Error storing conversation after error: {store_error}")
                                    print("Full traceback:")
                                    print(traceback.format_exc())
                         
                
            except KeyboardInterrupt:
                print("\n=== KEYBOARD INTERRUPT DETECTED ===")
                print("Stopping the voice agent...")
                # Print final message summary
                print("\nFinal Message Summary:")
                print("---------------------")
                print(get_summary())
                break
            except Exception as e:
                print(f"\nError in main loop: {e}")
                print("Full traceback:")
                print(traceback.format_exc())
                break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n=== PROGRAM TERMINATED BY USER ===")
    except Exception as e:
        print(f"\n=== PROGRAM ERROR ===")
        print(f"Error: {e}")
        print("Full traceback:")
        print(traceback.format_exc()) 