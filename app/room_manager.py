import os
from livekit import rtc
from dotenv import load_dotenv
from .token_generator import generate_token

load_dotenv()

class RoomManager:
    def __init__(self):
        self.url = os.getenv("LIVEKIT_URL")

        identity = os.getenv("AGENT_NAME")
        self.token = generate_token(identity)

        self.room = rtc.Room()

    async def connect(self):
        await self.room.connect(self.url, self.token)
        print("Connected to LiveKit room")

        @self.room.on("participant_connected")
        def on_participant_connected(participant: rtc.RemoteParticipant):
            print(f"User joined: {participant.identity}")

        @self.room.on("track_subscribed")
        def on_track_subscribed(track, publication, participant):
            if isinstance(track, rtc.RemoteAudioTrack):
                print("Subscribed to audio track")
                self.handle_audio_track(track)

    def handle_audio_track(self, track: rtc.RemoteAudioTrack):
        import asyncio
        from livekit import rtc

        async def receive_audio():
            stream = rtc.AudioStream(track)

            async for frame in stream:
                print("Receiving audio frame...")

        asyncio.create_task(receive_audio())