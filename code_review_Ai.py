import os
from dotenv import load_dotenv
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ GEMINI_API_KEY not found. Add it in your .env file.")

# 2. Initialize Gemini (Pro Model)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",  # Gemini 2.5 Pro
    google_api_key=api_key,
    temperature=0.2
)

print("\n🔹 Gemini Universal Code Reviewer (Prototype)")
print("Paste your code snippet below (any language).")
print("👉 Press ENTER twice when done:\n")

# 3. Collect multi-line snippet
lines = []
while True:
    try:
        line = input()
        if line.strip() == "":  # blank line = end input
            break
        lines.append(line)
    except EOFError:
        break

code_snippet = "\n".join(lines)
if not code_snippet.strip():
    print("⚠️ No code snippet entered. Exiting.")
    exit()

# 4. Detect Language using Pygments
def detect_language_pygments(code: str) -> tuple:
    try:
        lexer = guess_lexer(code)
        return lexer.name, 0.8  # Assume 80% confidence if detected
    except ClassNotFound:
        return "Unknown", 0.0

# 5. Detect Language using Gemini
def detect_language_gemini(code: str) -> tuple:
    prompt = f"Detect the programming language of this code snippet:\n{code}\nAnswer with only the language name."
    response = llm.invoke(prompt)
    gemini_lang = response.content.strip()
    return gemini_lang, 0.9  # Assume Gemini is highly confident

pygments_lang, pygments_conf = detect_language_pygments(code_snippet)
gemini_lang, gemini_conf = detect_language_gemini(code_snippet)

# 6. Decide Best Match
if pygments_lang == "Unknown":
    final_lang = gemini_lang
    confidence = gemini_conf
elif gemini_lang.lower() == pygments_lang.lower():
    final_lang = pygments_lang
    confidence = (pygments_conf + gemini_conf) / 2
else:
    # If disagreement, pick the higher confidence one
    if gemini_conf > pygments_conf:
        final_lang = gemini_lang + " (Gemini guess)"
        confidence = gemini_conf
    else:
        final_lang = pygments_lang + " (Pygments guess)"
        confidence = pygments_conf

print(f"\n📌 Pygments detected: {pygments_lang} ({pygments_conf*100:.0f}% confidence)")
print(f"📌 Gemini detected: {gemini_lang} ({gemini_conf*100:.0f}% confidence)")
print(f"\n✅ Final Language: {final_lang} (Confidence: {confidence*100:.0f}%)\n")

# 7. Send to Gemini for Review
prompt = f"""
You are a code reviewer. The following code is written in **{final_lang}**.

Tasks:
- Identify bugs or errors
- Suggest improvements (style, performance, readability, best practices, security)
- If possible, provide a corrected or optimized version

Code Snippet:
{code_snippet}
"""

response = llm.invoke(prompt)

# 8. Output result
print("\n===== Gemini Review =====\n")
print(response.content)
