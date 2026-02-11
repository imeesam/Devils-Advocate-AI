from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
	print("⚠️ GEMINI_API_KEY not set in environment; aborting test")
	raise SystemExit(1)

client = genai.Client(api_key=api_key)



# Test Gemini 2.5 Flash Lite (stable, lower token usage)
print("\nTesting Gemini 2.5 Flash Lite...")
resp = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="What is 2+2? Explain simply."
)
print(f"Gemini 2.5 Flash Lite: {resp.text[:100]}...")

