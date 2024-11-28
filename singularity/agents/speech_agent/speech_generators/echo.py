from openai import OpenAI

from src.agents.speech_agent.speech_generators.speach_generator_base import SpeechGeneratorBase
from src.common.config import singularity_config
from src.common.types import ModelType


class Echo(SpeechGeneratorBase):
    MODEL_NAME = ModelType.GPT4
    VERSION = ('tts-1',)
    VOICE = ('echo',)

    def __init__(self):
        self.client = OpenAI(api_key=singularity_config.settings.OPEN_AI_KEY)

    def _generate_audio(self, text):
        with self.client.audio.speech.with_streaming_response.create(
            model='tts-1',
            voice='alloy',
            input=text,
        ) as response:
            return response.read()

    def _parse_response(self, response):
        return response
