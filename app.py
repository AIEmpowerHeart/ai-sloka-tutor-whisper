
import streamlit as st
import os
import zipfile
import tempfile
import whisper
from pathlib import Path
from io import BytesIO
from fpdf import FPDF

# Title and intro
st.set_page_config(page_title="AI Sloka Tutor", layout="centered")
st.title("🧘 AI Sloka Tutor (Whisper-Powered)")
st.write("Upload Sanskrit sloka audio (.wav or ZIP) to transcribe and reflect.")

# Chapter & Sloka dropdown
chapter = st.selectbox("Select Chapter", [f"Chapter {i}" for i in range(1, 19)])
sloka_num = st.selectbox("Select Sloka Number", [f"Sloka {i}" for i in range(1, 51)])

uploaded_file = st.file_uploader("📤 Upload .wav file or .zip of .wav files", type=["wav", "zip"])

if uploaded_file:
    audio_files = []

    if uploaded_file.name.endswith(".zip"):
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            extract_path = tempfile.mkdtemp()
            zip_ref.extractall(extract_path)
            audio_files = list(Path(extract_path).rglob("*.wav"))
    else:
        temp_path = Path(tempfile.mktemp(suffix=".wav"))
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        audio_files = [temp_path]

    st.success(f"{len(audio_files)} audio file(s) ready for transcription.")
    model = whisper.load_model("base")

    transcripts = []
    for i, audio_path in enumerate(audio_files):
        st.audio(str(audio_path), format='audio/wav')
        with st.spinner(f"Transcribing file {i+1}/{len(audio_files)}..."):
            result = model.transcribe(str(audio_path))
            st.subheader(f"📜 Transcription {i+1}")
            st.success(result["text"])
            transcripts.append(f"{audio_path.name}:
{result['text']}\n")

    # Reflection
    st.subheader("🧠 Reflect after listening:")
    st.text_area("What did you understand from the sloka?", key="reflection")

    # Export
    export_format = st.radio("Download Transcripts As", ["Text (.txt)", "PDF (.pdf)"])
    if st.button("📥 Export Transcript(s)"):
        if export_format == "Text (.txt)":
            output = BytesIO("\n".join(transcripts).encode())
            st.download_button("Download TXT", output, file_name="transcripts.txt")
        else:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in "\n".join(transcripts).split("\n"):
                pdf.cell(200, 10, txt=line, ln=True)
            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)
            st.download_button("Download PDF", pdf_output, file_name="transcripts.pdf")
