import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI()

audio_file= open("recording.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
)

print(transcription.text)

