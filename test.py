import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Test Gemini 3 Flash
print("Testing Gemini 3 Flash Preview...")
model_flash = genai.GenerativeModel('gemini-3-flash-preview')
response = model_flash.generate_content("What is 2+2? Explain simply.")
print(f"Gemini 3 Flash: {response.text[:100]}...")

# Test Gemini 3 Pro
print("\nTesting Gemini 3 Pro Preview...")
model_pro = genai.GenerativeModel('gemini-3-pro-preview')
response = model_pro.generate_content("What is 2+2? Explain simply.")
print(f"Gemini 3 Pro: {response.text[:100]}...")

print("\n✅ Gemini 3 models are working!")