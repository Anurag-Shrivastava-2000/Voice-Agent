# Real-Time Voice Agent (LiveKit + OpenAI)

## Overview

This project implements a real-time voice agent that joins a LiveKit room and interacts with users through speech.

The agent:

- Connects to a LiveKit room as a participant  
- Subscribes to remote audio tracks  
- Uses Voice Activity Detection (VAD) to detect speech boundaries  
- Converts speech to text using OpenAI Speech-to-Text (STT)  
- Generates spoken responses using OpenAI Text-to-Speech (TTS)  
- Publishes audio responses back into the LiveKit room  

The system behaves like a real conversational participant in a live audio session.

---

##  Architecture

User Microphone  
        ↓  
LiveKit Room  
        ↓  
Voice Agent  
        ↓  
[VAD] → Detect speech boundaries  
        ↓  
[STT] → Transcription (OpenAI)  
        ↓  
Response Generation  
        ↓  
[TTS] → Speech synthesis (OpenAI)  
        ↓  
LiveKit Audio Publish  

---

## ✅ Features Implemented

- Real-time LiveKit room connection  
- Automatic subscription to remote audio tracks  
- Voice Activity Detection using WebRTC VAD  
- Minimum speech duration guard to prevent short/noisy transcriptions  
- Speech-to-Text transcription using OpenAI  
- Text-to-Speech response generation using OpenAI  
- Audio publishing back into the LiveKit room  
- Modular and clean project structure  

---

## 📂 Project Structure

voice-agent/  
│  
├── app/  
│   ├── __init__.py  
│   ├── main.py  
│   ├── token_generator.py  
│   ├── vad.py  
│   ├── audio_buffer.py  
│   ├── stt.py
│   ├── generate_user_token.py
│   └── tts.py  
│ 
├── requirements.txt  
├── .env.example  
└── README.md  

---

## Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <repository-url>
cd voice-agent
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file using `.env.example`:

```
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_API_SECRET=
ROOM_NAME=agent-room
AGENT_NAME=voice-agent
OPENAI_API_KEY=
```

---

### 5️⃣ Run the Voice Agent

```bash
python -m app.main
```

---

### 6️⃣ Connect from Browser

1. Go to: https://meet.livekit.io  
2. Use **Custom** connection  
3. Enter your LiveKit Server URL  
4. Generate a token using:

```bash
python -m app.generate_user_token
```

5. Paste the token into LiveKit Meet  
6. Join the same room  

---

## 🧠 How It Works

### Voice Activity Detection (VAD)

- Audio frames are streamed from LiveKit.  
- 10ms frame alignment is performed for compatibility with WebRTC VAD.  
- Speech boundaries are detected in real time.  

### Speech Buffering

- Full PCM audio is buffered while speech is active.  
- A minimum duration threshold prevents short/invalid segments.  

### Speech-to-Text

- Buffered PCM audio is wrapped into WAV format.  
- Sent to OpenAI `gpt-4o-mini-transcribe`.  
- Transcript returned as text.  

### Text-to-Speech

- Response generated using OpenAI `gpt-4o-mini-tts`.  
- Audio returned and published back to LiveKit.  

---

## Example Interaction

User says:

> Hello

Agent response:

> You said: Hello

---

## Known Limitations

- TTS playback is sent as a single frame (can be optimized using streaming frames).  
- No long-term conversation memory.  
- Silence reminder feature is not implemented.  
- Interruption cancellation can be further improved.  

---

## Future Improvements

- Streaming STT instead of batch transcription  
- Real-time streaming TTS playback  
- Conversation state management  
- Silence detection reminders  
- Interruption-aware cancellation  
- Minimal web UI for monitoring state and transcripts  

---

## Assignment Compliance

This implementation satisfies:

- Real-time LiveKit room participation  
- Audio-only communication  
- No overlapping audio publishing logic  
- Speech boundary detection using VAD  
- Clean modular structure  
- Clear setup documentation  

---

## Technologies Used

- Python  
- LiveKit Python SDK  
- OpenAI SDK  
- WebRTC VAD  
- asyncio (real-time event handling)  

---

## 👤 Author

Anurag Shrivastava  
Real-Time Voice Agent Implementation  
