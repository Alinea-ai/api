from abc import ABC, abstractmethod

from src.agents.transcriber_agent.exceptions import TranscriberError, TranscriberParserError


class TranscriberBase(ABC):
    MODEL_NAME = 'base'
    transcriber_by_model = {}

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        if cls.MODEL_NAME:
            cls.transcriber_by_model[cls.MODEL_NAME] = cls

    @classmethod
    def get_transcriber_by_model(cls, model):
        return cls.transcriber_by_model.get(model.model_name)()

    @abstractmethod
    def _transcribe(self, audio):
        """Transcribe audio"""

    @abstractmethod
    def _parse_response(self, response):
        """Parse response"""

    def parse_response(self, response):
        """Parse response"""
        try:
            return self._parse_response(response)
        except Exception as e:
            raise TranscriberParserError('Unexpected Error') from e

    def transcribe(self, audio):
        try:
            transcription = self._transcribe(audio)
            return self.parse_response(transcription)
        except Exception as e:
            raise TranscriberError(f'Unexpected Error: {e}') from e
