import os

from dotenv import load_dotenv
from google import genai


# Load environment variables from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the environment.")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send a simple test request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Respond with exactly: Gemini API connection successful."
)

print(response.text)