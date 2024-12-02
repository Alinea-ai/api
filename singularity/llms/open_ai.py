from langchain_openai import  ChatOpenAI


def get_opneai(model_name:str = "gpt-4", temperature:float = 0.5):
    return ChatOpenAI(
        openai_api_key='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',
        model_name=model_name,
        temperature=temperature
    )