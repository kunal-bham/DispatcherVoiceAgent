from setuptools import setup, find_packages

setup(
    name="dispatcher-voice-agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition==3.10.0",
        "pyaudio==0.2.13",
        "openai==1.12.0",
        "python-dotenv==1.0.0",
        "soundfile==0.12.1",
        "numpy==1.24.3",
        "scipy==1.10.1",
        "httpx"
    ],
) 