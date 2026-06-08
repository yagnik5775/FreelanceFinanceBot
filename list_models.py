from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

print("✅ Available models for generateContent:\n")
for model in client.models.list():
    # Only show models that support generateContent
    if 'generateContent' in str(model.supported_actions):
        print(f"  {model.name}")