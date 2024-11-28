import io
from pathlib import Path

from src.agents.agent_base import AgentBase
from src.agents.transcriber_agent.exceptions import TranscriberFileNotFoundError
from src.agents.transcriber_agent.transcribers.transcriber_base import TranscriberBase


class TranscriberAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.transcriber = TranscriberBase.get_transcriber_by_model(self.model)

    def transcribe_audio_from_binary(self, audio_file):
        # Ensure the file's pointer is at the beginning
        audio_file.file.seek(0)
        buffer = io.BytesIO(audio_file.file.read())
        buffer.name = 'file.mp3'
        transcription = self.transcriber.transcribe(buffer)

        return transcription

    def transcribe_audio_from_file(self, audio_file_path: str):
        # TODO: option to get file from S3
        path = Path(audio_file_path)
        if not path.is_file():
            raise TranscriberFileNotFoundError(f'Audio file not found: {audio_file_path}')

        with path.open('rb') as audio_file:
            transcription = self.transcriber.transcribe(audio=audio_file)

        return transcription

    def invoke(self, query: str):
        pass


if __name__ == '__main__':
    agent = TranscriberAgent()
    print(agent.transcribe_audio_from_file('sample_audio.wav'))
