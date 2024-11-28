from collections.abc import Buffer

from src.agents.agent_base import AgentBase
from src.agents.speech_agent.speech_generators import SpeechGeneratorBase


class SpeechAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.tts = SpeechGeneratorBase.get_tts_by_model(self.model)

    def invoke(self, text: str) -> Buffer:
        return self.tts.generate_audio(text)


if __name__ == '__main__':
    agent = SpeechAgent()
    response = agent.invoke('hello')
    print(response)
