from typing import Any

from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy.exc import OperationalError

from src.agents.agent_base import AgentBase
from src.agents.sql_agent.exceptions import (
    SqlAgentConnectionError,
    SqlAgentResponseParserError,
    SqlAgentUnexpectedError,
)
from src.common.config import LOCAL_CONFIG
from src.common.logger import Logger
from src.models.config import Config


class SqlAgent(AgentBase):
    def __init__(self, model_name: str = 'gpt-4', verbose: bool = False):
        super().__init__(model_name)
        self.logger = Logger(self)
        self.schema = None

    def get_sql_connect(self, config: Config) -> SQLDatabase | None:
        try:
            return SQLDatabase.from_uri(config.get_database_uri())
        except OperationalError as e:
            raise SqlAgentConnectionError(f'Failed to connect to: {config.get_database_uri()}, {e}')

    def pre_exec_prompt(self, query: str, db_context: dict[str, Any], config: Config) -> str:
        # TODO: Let's move this to use Jinja
        prompt = f"""
            You are sql expert I need you translate this human query into a SQL language.

            Based on human query, database type and database context
            human query: {query}
            database type: {config.type.value}
            database context: {db_context}

            Important always make sure to wrap your response with the symbol @
            at the beginning and the end of the response.
            example:
            @ <your response > @

            Identify language of query, for example english or spanish.
            Return sql query and language in this format
            example:
            @
            sql: SELECT * from users limit 5
            language: spanish
            @
            Just return sql query and language in this format, no need for more explanation

            If it is not possible to translate query to sql dialect, please return like example bellow,
            and use a friendly message informing why it is not possible to translate.
            @
            sql: None
            language: english
            error: True
            message: reason why it can't be translated
            @

            if query include any destructive statements, like UPDATE, INSERT, DELETE, DROP then return like
            example bellow, and add message saying
            somthing funny and friendly informing user that you can only create non-destructive queries.
            @
            sql: None
            language: english
            error: True
            message: reason why it can't be translated
            @
            """
        return prompt

    def post_exec_prompt(self, query: str, query_result: str, language: str) -> str:
        prompt = f"""
            Based on query and results return in
            human like response using language

            query: {query}
            results: {query_result}
            language: {language}
            """
        return prompt

    def query_model(self, prompt: str):
        return self.model.invoke(prompt)

    def translate_to_sql(self, config: Config, sql_conn, human_query: str) -> dict:
        if self.schema is None:
            self.schema = sql_conn.get_context()
            print(self.schema)
        prompt = self.pre_exec_prompt(human_query, self.schema, config=config)
        model_response = self.query_model(prompt)
        # TODO: we can access token usage like so: model_response.token_usage["total_tokens"]
        #  let's save it along with prompt, query, and response as metadata
        try:
            return self.parse_generic(model_response.content)
        except Exception as e:
            raise SqlAgentResponseParserError() from e

    def analyze_response(self, query: str, query_result: str, language: str) -> str:
        prompt = self.post_exec_prompt(query, query_result, language)

        return self.query_model(prompt)

    def invoke(self, query: str, db_config: Config = None) -> tuple[str, str | None]:
        self.logger.info(f'Starting with prompt: {query}')
        sql_conn = self.get_sql_connect(db_config or LOCAL_CONFIG)

        try:
            sql_query = self.translate_to_sql(config=db_config, sql_conn=sql_conn, human_query=query)
            if 'error' in sql_query:
                return sql_query['message'], None

            self.logger.info(f"SQL Query: {sql_query['sql']}")
            results = sql_conn.run(sql_query['sql'])
            response = self.analyze_response(query, results, sql_query['language'])

            return ' '.join(response.content.split()), sql_query.get('sql')
        except Exception as e:
            raise SqlAgentUnexpectedError(f'Failed to invoke with: {e}') from e
