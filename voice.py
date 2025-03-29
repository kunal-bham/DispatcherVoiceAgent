# from flask import Flask, request, Response
# from flask import Flask, request
# from twilio.twiml.voice_response import VoiceResponse
# from twilio.rest import Client
# import os
# from dotenv import load_dotenv


# load_dotenv()

# app = Flask(__name__)

# # export TWILIO_ACCOUNT_SID=AC02f60de55c2e9d406973f41cd48dc3be
# TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
# # export TWILIO_AUTH_TOKEN=e5b61f04393725d8c1c3dea81779c0d4
# TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
# TWILIO_PHONE_NUMBER = '+18447948347'

# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# def update_phone_webhook(webhook_url):
#     """Update the Twilio phone number's webhook URL"""
#     try:
#         phone_number = client.incoming_phone_numbers.list(
#             phone_number=TWILIO_PHONE_NUMBER)[0]
#         phone_number.update(
#             voice_url=webhook_url,
#             voice_method='POST'
#         )
#         print(f"Successfully updated webhook URL to: {webhook_url}")
#     except Exception as e:
#         print(f"Error updating webhook URL: {e}")


# @app.route("/answer", methods=['POST'])
# def answer_call():
#     resp = VoiceResponse()
#     print(resp)

#     dial = resp.dial(callerId=TWILIO_PHONE_NUMBER)

#     if request.values.get('To') == TWILIO_PHONE_NUMBER:
#         resp.say(
#             "Hello! This is your emergency dispatch system. How can I help you today?")

#         gather = resp.gather(
#             input='speech', action='/handle-input', method='POST')

#     return str(resp)


# @app.route("/handle-input", methods=['POST'])
# def handle_input():
#     speech_result = request.values.get('SpeechResult', '')

#     resp = VoiceResponse()

#     resp.say(f"I heard you say: {speech_result}")

#     resp.say("Is there anything else I can help you with?")

#     gather = resp.gather(input='speech', action='/handle-input', method='POST')

#     return str(resp)


# if __name__ == "__main__":
#     # When you start the app, you can update the webhook URL
#     # Replace this with your ngrok URL when you start ngrok
#     # webhook_url = "https://your-ngrok-url.ngrok.io/answer"
#     # update_phone_webhook(webhook_url)
#     app.run(debug=True, port=5000)

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
