import os
import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ GEMINI_API_KEY not found. Add it in .env file.")

# 2. Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=api_key)

def review_code(code_snippet: str, filename: str):
    """Send code/text to Gemini for review"""
    prompt = f"""
    You are a code reviewer. Review the following snippet from `{filename}`.
    Tasks:
    - Identify bugs or errors
    - Suggest improvements (style, performance, readability, best practices, security)
    - If possible, provide a corrected or optimized version

    Code/Text Snippet:
    {code_snippet}
    """

    response = llm.invoke(prompt)
    print("\n===== Gemini Review =====\n")
    print(response.content)

def main():
    if len(sys.argv) < 2:
        print("⚠️ Usage: python reviewer.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        sys.exit(1)

    # Read the file
    with open(filename, "r", encoding="utf-8") as f:
        code_snippet = f.read()

    if not code_snippet.strip():
        print("⚠️ The file is empty.")
        sys.exit(1)

    # Review file content
    review_code(code_snippet, filename)

if __name__ == "__main__":
    main()
