# DispatcherVoiceAgent
HooHacks25


Run `pip install -r requirements.txt`

Run `python voice_agent.py`

Pasted over from Devpost:

# What it does
QuickCall911 is an AI emergency dispatcher that can be deployed when there is not enough human dispatchers. It follows a guide similar to human dispatchers and gives advice to people and then when a human dispatcher is available it will get switched out and will send a summarization of the conversation to the human dispatcher to get caught up. QuickCall911 is also being developed to be proficient in 16 languages so that it can meet the needs of people who don't speak English.

# How we built it
1. **Core Voice Agent Setup**
   - Created a Python-based voice agent implementing OpenAI's Whisper API for transcription
   - Set up text-to-speech capabilities for responses
   - Created conversation flow with AI response trained for emergency dispatch
   - Added 16 language capabilities

2. **Retrieval Augmented Generation (RAG) system**
   - Created a knowledge base with emergency protocols, location data, and medical guidelines
   - Set up semantic search capabilities for retrieving relevant information
   - Configured response generation with specific emergency handling protocols

3. **MongoDB integration for storing conversation history**
   - Implemented call summary generation functionality

4. **Web Interface Development**
   - Created an Express.js server for the web interface
   - Built a website that can display MongoDB updates in real time

# Challenges we ran into
1. We had trouble with Twilio because the free version did not allow for conversational responses on the phone, so we had to pivot and host the model locally.
2. We also ran into trouble with the prompt engineering and getting the AI to give logical and timely responses
3. Making the TTS agent work quickly for long caller responses

# Accomplishments that we're proud of
1. We built a RAG to improve upon the existing LLM.  
2. Getting multilingual support for the agent  
3. Allowing the entire project flow to work in real-time (making it useful in a real emergency)  
4. Implementing the seamless transitioning to human dispatchers  
5. The UI

# What we learned
1. How to implement RAG with a voice agent
2. Creating voice agents that can speak multiple languages
3. Working with Twilio API

# What's next for QuickCall911
1. Improve RAG functionality
2. Make the voice agent sound more human-like
3. Train the agent to detect and be fluent in more languages
