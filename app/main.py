import asyncio
import os
import io
import wave
from dotenv import load_dotenv
from livekit import rtc

from .token_generator import generate_token
from .vad import VADDetector
from .audio_buffer import AudioBuffer
from .stt import SpeechToText
from .tts import TextToSpeech

load_dotenv()


class VoiceAgent:
    def __init__(self):
        self.url = os.getenv("LIVEKIT_URL")
        self.identity = os.getenv("AGENT_NAME")
        self.room_name = os.getenv("ROOM_NAME")

        self.token = generate_token(self.identity)
        self.room = rtc.Room()

        self.vad = VADDetector(2)
        self.buffer = AudioBuffer()
        self.stt = SpeechToText(os.getenv("OPENAI_API_KEY"))
        self.tts = TextToSpeech(os.getenv("OPENAI_API_KEY"))

        self.speaking = False

        self.audio_source = rtc.AudioSource(48000, 1)
        self.local_track = rtc.LocalAudioTrack.create_audio_track(
            "agent-voice", self.audio_source
        )

    async def connect(self):
        await self.room.connect(
            self.url,
            self.token,
            options=rtc.RoomOptions(auto_subscribe=True),
        )

        print("Connected to LiveKit room")
        print("Room name (agent):", self.room.name)

        await self.room.local_participant.publish_track(self.local_track)

        # Handle already connected participants
        for participant in self.room.remote_participants.values():
            print("Existing participant found:", participant.identity)
            self.subscribe_to_participant(participant)

        @self.room.on("participant_connected")
        def on_participant_connected(participant: rtc.RemoteParticipant):
            print(f"User joined: {participant.identity}")
            self.subscribe_to_participant(participant)

        @self.room.on("track_subscribed")
        def on_track_subscribed(track, publication, participant):
            if isinstance(track, rtc.RemoteAudioTrack):
                print(f"Subscribed to audio track from {participant.identity}")
                asyncio.create_task(self.receive_audio(track))

    def subscribe_to_participant(self, participant):
        for publication in participant.track_publications.values():
            if publication.track and isinstance(publication.track, rtc.RemoteAudioTrack):
                print("Manually subscribing to existing audio track")
                asyncio.create_task(self.receive_audio(publication.track))

    async def receive_audio(self, track: rtc.RemoteAudioTrack):
        stream = rtc.AudioStream(track)

        vad_buffer = b""
        full_audio_buffer = b""

        async for event in stream:
            audio_frame = event.frame
            pcm_data = audio_frame.data

            # Always collect full raw audio
            full_audio_buffer += pcm_data

            # Accumulate for VAD (10ms frames = 960 bytes at 48kHz)
            vad_buffer += pcm_data

            if len(vad_buffer) < 960:
                continue

            frame_for_vad = vad_buffer[:960]
            vad_buffer = vad_buffer[960:]

            try:
                is_speech = self.vad.is_speech(frame_for_vad, sample_rate=48000)
            except Exception:
                continue

            if is_speech:
                if not self.speaking:
                    self.speaking = True
                    full_audio_buffer = b""  # reset when speech starts
                    print("Speech started")

            else:
                if self.speaking:
                    self.speaking = False
                    print("Speech ended")

                    audio_segment = full_audio_buffer
                    full_audio_buffer = b""

                    print("Audio segment size:", len(audio_segment))

                    # Minimum ~0.4 seconds of audio required
                    if len(audio_segment) < 40000:
                        print("Audio too short, skipping STT")
                        continue

                    try:
                        transcript = self.stt.transcribe(audio_segment)
                        print("Transcript:", transcript)
                    except Exception as e:
                        print("STT Error:", e)
                        continue

                    response_text = f"You said: {transcript}"
                    await self.respond(response_text)

    async def respond(self, text: str):
        print("Generating TTS...")

        wav_bytes = self.tts.synthesize(text)

        print("Playing response...")

        await self.audio_source.capture_frame(rtc.AudioFrame(data=wav_bytes,sample_rate=48000,num_channels=1,samples_per_channel=len(wav_bytes) // 2,))


async def main():
    agent = VoiceAgent()
    await agent.connect()

    while True:
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())