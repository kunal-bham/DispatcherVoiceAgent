# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import os
import assemblyai as aai

# Get API key from environment variable
api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not api_key:
    raise ValueError("Please set the ASSEMBLYAI_API_KEY environment variable")

aai.settings.api_key = api_key
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("https://assembly.ai/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)