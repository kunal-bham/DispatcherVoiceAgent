"""
python voice.py
ngrok http 500
copy forwarding link onto webhook with /voice on Twilio
"""

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from src.ai_handler import get_ai_response, messages

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
    response.say("Thank you. We're processing your message.")
    
    return Response(str(response), mimetype='text/xml')

@app.route("/transcription-callback", methods=['POST'])
async def transcription_callback():
    transcription = request.form.get('TranscriptionText')
    if transcription:
        print(f"Transcription received: {transcription}")
        # Get AI response
        ai_response = await get_ai_response(transcription, messages)
        print(f"AI Response: {ai_response}")
        
        # Create a new TwiML response to speak the AI response
        response = VoiceResponse()
        response.say(ai_response)
        return Response(str(response), mimetype='text/xml')
    else:
        print("No transcription received")
        response = VoiceResponse()
        response.say("I'm sorry, but I couldn't understand what you said.")
        return Response(str(response), mimetype='text/xml')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
