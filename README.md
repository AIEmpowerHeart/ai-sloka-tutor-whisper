
# AI Sloka Tutor Whisper Batch

An AI-powered Sanskrit sloka tutor built using Streamlit and Whisper (offline mode) for transcription of `.wav` audio files.

## 🌟 Features

- Upload single `.wav` or batch `.zip` of sloka audio files
- Whisper-based transcription (no OpenAI API key required)
- Audio preview player
- Dropdown selection for Chapter & Sloka
- Export transcripts to PDF or plain text
- Mobile-optimized and Streamlit Cloud-ready

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 File Structure

- `app.py` - Main Streamlit app
- `.streamlit/config.toml` - Streamlit UI settings
- `.streamlit/secrets.toml` - Optional GPT key (future upgrade)
