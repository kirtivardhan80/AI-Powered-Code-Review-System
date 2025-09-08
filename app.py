import streamlit as st
import prototype as proto  # ✅ Import shared logic

# Streamlit Page Config
st.set_page_config(page_title="AI Code Review Tool", page_icon="🤖", layout="wide")
st.title("🤖 AI Code Review Tool")

# File uploader
uploaded_file = st.file_uploader(
    "Upload code file", 
    type=["py","java","cpp","c","js","ts","php","go","rb","kt","swift","txt"]
)

# Code input area
code_input = st.text_area("Or paste your code here:", height=300)

# Replace input with uploaded file content
if uploaded_file is not None:
    code_input = uploaded_file.read().decode("utf-8")
    st.success(f"Uploaded: {uploaded_file.name}")

# Analyze button
if st.button("🔍 Analyze Code"):
    if not code_input.strip():
        st.error("Please enter or upload code before analyzing.")
    else:
        with st.spinner("Detecting language..."):
            final_lang, conf, pyg_lang, pyg_conf, gem_lang, gem_conf = proto.determine_final_language(code_input)

        st.info(f"📌 Pygments detected: {pyg_lang} ({pyg_conf*100:.0f}% confidence)")
        st.info(f"📌 Gemini detected: {gem_lang} ({gem_conf*100:.0f}% confidence)")
        st.success(f"✅ Final Language: {final_lang} (Confidence: {conf*100:.0f}%)")

        with st.spinner("Analyzing code with Gemini..."):
            review = proto.generate_review(code_input, final_lang)

        st.subheader("✅ Gemini Code Review Result")
        st.write(review)
