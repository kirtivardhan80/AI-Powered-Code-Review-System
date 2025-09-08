from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Print Gemini API key to check
api_key = os.getenv("GEMINI_API_KEY")
print("Gemini API Key:", api_key)
 