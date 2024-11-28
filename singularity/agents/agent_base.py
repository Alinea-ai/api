import ast
import re
from abc import ABC, abstractmethod

from langchain_openai import ChatOpenAI

from src.common.config import singularity_config
from src.common.types import ModelType


class AgentBase(ABC):
    TEMPERATURE = 0
    MAX_TOKENS = -1
    model_types = ModelType

    def __init__(self, model_name: str = None):
        self.model_name = model_name or self.model_types.GPT4
        self.model = ChatOpenAI(api_key=singularity_config.settings.OPEN_AI_KEY, model_name=self.model_name)

    @abstractmethod
    def invoke(self, query: str, **kwargs):
        """main interface"""

    @staticmethod
    def convert_value(value: str):
        """
        Convert string representations of 'True', 'False', 'None', lists, and dicts
        to their respective Python types using ast.literal_eval for lists and dicts.
        """
        if value == 'True':
            return True
        elif value == 'False':
            return False
        elif value == 'None':
            return None
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value

    def parse_generic(self, input_str: str) -> dict:
        # Extract the content enclosed between the first pair of '@' symbols
        match = re.search(r'@(.+?)@', input_str, re.DOTALL)
        if not match:
            return {}

        content = match.group(1)

        # Find all key-value pairs within the content
        # Keys and values are separated by a colon, and pairs by newlines or other non-keyword characters
        pairs = re.findall(r'(\w+)\s*:\s*([^\n]+)', content)

        # Convert the list of pairs into a dictionary
        result_dict = {key.strip(): self.convert_value(value.strip()) for key, value in pairs}

        return result_dict
