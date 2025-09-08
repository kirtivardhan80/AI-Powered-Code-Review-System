import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ GEMINI_API_KEY not found. Add it in your .env file.")

# Gemini client
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=api_key,
    temperature=0.2
)

# Retry wrapper
def safe_invoke(prompt, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return llm.invoke(prompt)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay * (2 ** attempt))  # exponential backoff
            else:
                return f"❌ Failed after {retries} retries: {e}"

# Generate review
def generate_review(code: str, language: str):
    prompt = f"""
    You are a senior software engineer reviewing the following **{language}** code.

    Tasks:
    1. Identify bugs or logical errors
    2. Suggest improvements (style, performance, readability, best practices, security)
    3. Provide a corrected/optimized version if possible

    Code Snippet:
    {code}

    --- Format your response like this ---
    🔍 **Issues Found:**
    - ...

    ✅ **Suggestions:**
    - ...

    📝 **Improved Version:**
    ```{language}
    # improved code here
    ```
    ---------------------------------------
    """

    response = safe_invoke(prompt)

    if hasattr(response, "content"):
        review = response.content.strip()
    elif isinstance(response, str):
        review = response.strip()
    else:
        review = ""

    # Fallback if Gemini still fails
    if not review or review.strip() == "":
        return "⚠️ Gemini did not return a review, but the code looks valid."

    return review

# Language detection: Pygments
def detect_language_pygments(code: str):
    try:
        lexer = guess_lexer(code)
        return lexer.name, 0.8
    except ClassNotFound:
        return "Unknown", 0.0

# Language detection: Gemini
def detect_language_gemini(code: str):
    prompt = f"Detect the programming language of this code snippet:\n{code}\nAnswer with only the language name."
    response = safe_invoke(prompt)
    return response.content.strip(), 0.9 if hasattr(response, "content") else ("Unknown", 0.0)

# Decide final language
def determine_final_language(code: str):
    pyg_lang, pyg_conf = detect_language_pygments(code)
    gem_lang, gem_conf = detect_language_gemini(code)

    if pyg_lang == "Unknown":
        return gem_lang, gem_conf, pyg_lang, pyg_conf, gem_lang, gem_conf
    elif gem_lang.lower() == pyg_lang.lower():
        return pyg_lang, (pyg_conf + gem_conf) / 2, pyg_lang, pyg_conf, gem_lang, gem_conf
    else:
        if gem_conf > pyg_conf:
            return gem_lang + " (Gemini guess)", gem_conf, pyg_lang, pyg_conf, gem_lang, gem_conf
        else:
            return pyg_lang + " (Pygments guess)", pyg_conf, pyg_lang, pyg_conf, gem_lang, gem_conf

# ✅ Main function for FastAPI
def review_code(code: str):
    final_lang, confidence, pyg_lang, pyg_conf, gem_lang, gem_conf = determine_final_language(code)
    review = generate_review(code, final_lang)
    return {
        "final_language": final_lang,
        "confidence": confidence,
        "pygments_language": pyg_lang,
        "pygments_confidence": pyg_conf,
        "gemini_language": gem_lang,
        "gemini_confidence": gem_conf,
        "review": review
    }
