# DispatcherVoiceAgent
HooHacks25


Run `pip install -r requirements.txt`

Run `python voice_agent.py`

Pasted over from Devpost:

# What it does
QuickCall911 is an AI emergency dispatcher that can be deployed when there is not enough human dispatchers. QuickCall follows a guide similar to human dispatchers and gives advice to people and then when a human dispatcher is available it will get switched out and will send a summarization of the conversation to the human dispatcher to get caught up. QuickCall is also proficient in 16 languages so that it can meet the needs of people who don't speak English.

# How we built it
Core Voice Agent Setup
Created a Python-based voice agent implementing OpenAI's Whisper API for transcription
Set up text-to-speech capabilities for responses
Created conversation flow with AI response trained for emergency dispatch
Added 16 language capabilities
Retrieval Augmented Generation (RAG) system
Created a knowledge base with emergency protocols, location data, and medical guidelines
Set up semantic search capabilities for retrieving relevant information
Configured response generation with specific emergency handling protocols
MongoDB integration for storing conversation history
Implemented call summary generation functionality
Web Interface Development
Created an Express.js server for the web interface.
Built a website that can display MongoDB updates in real time.

# Challenges we ran into
We had trouble with Twilio because the free version did not allow for conversational responses on the phone, so we had to pivot and host the model locally.
We also ran into trouble with the prompt engineering and getting the AI to give logical and timely responses
Making the TTS agent work quickly for long caller responses

# Accomplishments that we're proud of
We built a RAG to improve upon the existing LLM.
Getting multilingual support for the agent
Allowing the entire project flow to work in real-time (making it useful in a real emergency)
Implementing the seamless transitioning to human dispatchers
The UI

# What we learned
How to implement RAG with a voice agent
Creating voice agents that can speak multiple languages
Working with Twilio API

# What's next for QuickCall911
Improve RAG functionality
Make the voice agent sound more human-like
Branch out to more languages
