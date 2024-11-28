from openai import OpenAI

from src.agents.transcriber_agent.transcribers.transcriber_base import TranscriberBase
from src.common.config import singularity_config
from src.common.types import ModelType


class Whisper(TranscriberBase):
    VERSION = 'whisper-1'
    MODEL_NAME = ModelType.GPT4

    def __init__(self):
        self.client = OpenAI(api_key=singularity_config.settings.OPEN_AI_KEY)

    def _transcribe(self, audio):
        return self.client.audio.transcriptions.create(file=audio, model=self.VERSION)

    def _parse_response(self, response):
        return response.text
