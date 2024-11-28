from abc import ABC, abstractmethod

from src.agents.speech_agent.exceptions import SpeechAgentError, SpeechAgentParserError


class SpeechGeneratorBase(ABC):
    MODEL_NAME = 'base'
    tts_by_model = {}

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        if cls.MODEL_NAME:
            cls.tts_by_model[cls.MODEL_NAME] = cls

    @classmethod
    def get_tts_by_model(cls, model):
        return cls.tts_by_model.get(model.model_name)()

    @abstractmethod
    def _generate_audio(self, text: str):
        """generates audio from text"""

    @abstractmethod
    def _parse_response(self, response):
        """Parse response"""

    def parse_response(self, response):
        """Parse response"""
        try:
            return self._parse_response(response)
        except Exception as e:
            raise SpeechAgentParserError('Unexpected Error') from e

    def generate_audio(self, text: str):
        try:
            audio_response = self._generate_audio(text)
            return self.parse_response(audio_response)
        except Exception as e:
            raise SpeechAgentError(f'Unexpected Error: {e}') from e
