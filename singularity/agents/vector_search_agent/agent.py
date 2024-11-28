from src.agents.agent_base import AgentBase
from src.common.logger import Logger
from src.vector_store.astra_store import AstraStore


class VectorSearchAgent(AgentBase):
    def __init__(self):
        super().__init__()
        self.vector_store = AstraStore()
        self.logger = Logger(self)

    def get_prompt(self, query, query_results):
        prompt = f"""
       Based on query and results return in human like response.
       Identify the language in query and return the response in the language.
       for example: if the language is english, return response in english.
       keep response not longer than 200 characters.

       query: {query}
       results: {query_results}
       """
        return prompt

    def invoke(self, query, collection=None):
        self.logger.info(f'Invoking VectorSearchAgent with query: {query}')
        context = self.vector_store.similarity_search(collection, query)
        if not context:
            context =  f'No results found for the query: {query}.'

        prompt = self.get_prompt(query, context)
        return self.model.invoke(prompt).content
