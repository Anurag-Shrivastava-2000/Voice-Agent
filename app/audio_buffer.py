class AudioBuffer:
    def __init__(self):
        self.frames = []

    def add_frame(self, frame):
        self.frames.append(frame)

    def clear(self):
        self.frames = []

    def get_audio(self):
        return b"".join(self.frames)

    def has_audio(self):
        return len(self.frames) > 0