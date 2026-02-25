import io
import wave
from openai import OpenAI


class SpeechToText:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def pcm_to_wav_file(self, pcm_data: bytes, sample_rate: int = 48000):
        buffer = io.BytesIO()

        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(sample_rate)
            wf.writeframes(pcm_data)

        buffer.seek(0)

        buffer.name = "speech.wav"

        return buffer

    def transcribe(self, pcm_data: bytes):
        wav_file = self.pcm_to_wav_file(pcm_data)

        transcript = self.client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=wav_file,
        )

        return transcript.text