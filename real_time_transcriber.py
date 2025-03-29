import speech_recognition as sr
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

def transcribe_audio(audio_data):
    """Transcribe audio using OpenAI's Whisper model"""
    response = openai.Audio.transcribe(
        "whisper-1",
        audio_data
    )
    return response["text"]

def main():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    print("Starting real-time transcription...")
    print("Press Ctrl+C to stop")
    
    with sr.Microphone() as source:
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Ready! Speak now...")
        
        while True:
            try:
                # Listen for audio input
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Save audio to temporary file
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Transcribe the audio
                with open("temp_audio.wav", "rb") as audio_file:
                    transcription = transcribe_audio(audio_file)
                    if transcription:
                        print(f"\nTranscription: {transcription}")
                
                # Clean up temporary file
                os.remove("temp_audio.wav")
                
            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                print("\nStopping transcription...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

if __name__ == "__main__":
    main() 