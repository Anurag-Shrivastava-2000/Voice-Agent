from openai import OpenAI


class TextToSpeech:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def synthesize(self, text: str) -> bytes:
        # Correct parameter name for our SDK
        response = self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
            response_format="wav",
        )

        return response.read()