"""
python voice.py
ngrok http 500
copy forwarding link onto webhook with /voice on Twilio
"""

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import os

app = Flask(__name__)


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    # Your custom phrase
    custom_phrase = "Hello. You’ve reached the emergency assistant. Please state your emergency after the beep."

    # TwiML response
    response = VoiceResponse()
    response.say(custom_phrase)
    response.pause(length=1)
    response.record(max_length=30, action="/handle-recording")

    return Response(str(response), mimetype='text/xml')


@app.route("/handle-recording", methods=['POST'])
def handle_recording():
    recording_url = request.form['RecordingUrl']
    print(f"New emergency call recording: {recording_url}")
    return "<Response><Say>Thank you. We’ve received your message.</Say></Response>"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
