
import streamlit as st
import os
import zipfile
import tempfile
import whisper
from utils import load_sloka_library, get_sloka_text, simple_explanation
from export import export_text, export_pdf

# Load Sloka library
sloka_data = load_sloka_library("slokas.json")

st.set_page_config(page_title="🧘 AI Sloka Tutor", layout="centered")
st.title("🧘 AI Sloka Tutor (Voice to Meaning)")
st.write("Upload a ZIP file of Sanskrit slokas in .wav format and select a chapter & sloka to transcribe and reflect.")

# Dropdowns
chapter = st.selectbox("📖 Select Chapter", list(sloka_data.keys()))
sloka_number = st.selectbox("🔢 Select Sloka", list(sloka_data[chapter].keys()))
sloka_details = get_sloka_text(sloka_data, chapter, sloka_number)

st.markdown(f"### 📜 Selected Sloka:
**Sanskrit:** {sloka_details['sanskrit']}

**Transliteration:** {sloka_details['transliteration']}

**Meaning:** {sloka_details['meaning']}")

# Upload ZIP of .wav files
uploaded_zip = st.file_uploader("📦 Upload ZIP containing .wav sloka audio files", type=["zip"])

if uploaded_zip:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "slokas.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
            wav_files = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir) if f.endswith(".wav")]

        for wav in wav_files:
            st.audio(wav, format='audio/wav')
            st.markdown(f"**🎧 File:** {os.path.basename(wav)}")
            with st.spinner("🔍 Transcribing..."):
                model = whisper.load_model("base")
                result = model.transcribe(wav)
                transcription = result["text"]

            st.subheader("📜 Transcription")
            st.success(transcription)

            st.subheader("💡 Explanation")
            st.info(simple_explanation(transcription))

            st.subheader("🪞 Your Reflection")
            reflection = st.text_area("What did you understand or feel after chanting/listening to this sloka?")
            if reflection:
                st.success("🌼 Beautiful! Reflect more often.")

            # Export options
            export_text(transcription, sloka_details)
            export_pdf(transcription, sloka_details)
