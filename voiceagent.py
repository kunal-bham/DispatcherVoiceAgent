# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import os
import assemblyai as aai
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import ollama

# Step 1: Speech to Text User to AI
# Step 2: Real-Time Transcription with AssemblyAI  
# Step 3: AI Response with GPT
# Step 4: Live Audio Streaming. Text-to-Speech with ElevenLabs

class AIVoiceAgent:
    def __init__(self):
        aai.settings.api_key = "ASSEMBLYAI_API_KEY"
        self.client = ElevenLabs(
            api_key = "ELEVENLABS_API_KEY"
        )

        self.transcriber = None

        self.full_transcript = [
            {"role":"system", "content":"You are a language model, answer the questions being asked in less than 300 characters."},
        ]





