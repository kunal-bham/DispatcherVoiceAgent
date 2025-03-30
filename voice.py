"""
python voice.py
ngrok http 500
copy forwarding link onto webhook with /voice on Twilio
"""

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from src.ai_handler import get_ai_response, messages
import asyncio
import os

app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    # Your custom phrase
    custom_phrase = "Hello. You've reached the emergency assistant. Please state your emergency after the beep."

    # TwiML response
    response = VoiceResponse()
    response.say(custom_phrase)
    response.pause(length=1)
    response.record(max_length=10, 
                   action="/handle-recording",
                   transcribe=True,
                   transcribeCallback="/transcription-callback")

    return Response(str(response), mimetype='text/xml')

@app.route("/handle-recording", methods=['POST'])
def handle_recording():
    recording_url = request.form.get('RecordingUrl')
    if not recording_url:
        print("No recording URL received")
        response = VoiceResponse()
        response.say("We're sorry, but we didn't receive your recording. Please try again.")
        return Response(str(response), mimetype='text/xml')
    
    print(f"New emergency call recording: {recording_url}")
    
    # Create a new TwiML response
    response = VoiceResponse()
    
    # Play back the recording
    #response.play(recording_url)
    
    
    
    # Add confirmation message
    response.say("Thank you. We've received your message and will process it shortly.")

   
    
    return Response(str(response), mimetype='text/xml')

@app.route("/transcription-callback", methods=['POST'])
def transcription_callback():
    transcription = request.form.get('TranscriptionText')
    if transcription:
        print(f"Transcription: {transcription}")
        # Create a new TwiML response to speak the transcription
        response = VoiceResponse()
        
        try:
            # Debug: Print environment variables
            print(f"Current working directory: {os.getcwd()}")
            print(f"OPENAI_API_KEY environment variable: {'Present' if os.getenv('OPENAI_API_KEY') else 'Missing'}")
            
            # Get AI response using asyncio.run
            ai_response = asyncio.run(get_ai_response(transcription, messages))
            print(f"AI Response: {ai_response}")
            if ai_response:
                # Create a new response for the AI message
                response = VoiceResponse()
                # Speak the AI response
                response.say(ai_response, voice="Polly.Amy")
                # Add a pause after the response
                response.pause(length=1)
                # Ask if they need anything else
                response.say("Is there anything else you need help with?", voice="Polly.Amy")
                print("Sending TwiML response:", str(response))
            else:
                response.say("I apologize, but I'm having trouble processing your request right now.")
        except Exception as e:
            print(f"Error getting AI response: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            response.say("I apologize, but I'm having trouble processing your request right now.")
            
        return Response(str(response), mimetype='text/xml')
    else:
        print("No transcription received")
        response = VoiceResponse()
        response.say("I'm sorry, but I couldn't understand what you said.")
        return Response(str(response), mimetype='text/xml')


if __name__ == "__main__":
    app.run(debug=True, port=5001)
