from typing import Any
from functools import lru_cache

from langchain_community.utilities.sql_database import SQLDatabase

from singularity.agents.agent_base import AgentBase
from singularity.agents.sql_agent.exceptions import SqlAgentConnectionError, \
    SqlAgentResponseParserError, SqlAgentUnexpectedError


class SqlAgent(AgentBase):
    def __init__(self, model_name: str = 'gpt-4', verbose: bool = False):
        super().__init__(model_name)
        self.schema = None
    @lru_cache(maxsize=1024)
    def get_sql_connect(self) -> SQLDatabase | None:
        uri = f'sqlite:////Users/latrealus/Documents/gits/api/db.sqlite3'
        try:
            return SQLDatabase.from_uri(uri)
        except Exception as e:
            raise SqlAgentConnectionError(f'Failed to connect to: {uri}, {e}')

    def pre_exec_prompt(self, query: str, db_context: dict[str, Any] = None) -> str:
        # TODO: Let's move this to use Jinja
        prompt = f"""
            You are sql expert I need you translate this human query into a SQL language.

            Based on human query, database type and database context if it is not None
            human query: {query}
            database type: sqllite
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

    def translate_to_sql(self, sql_conn, human_query: str, use_db_schema: bool = True) -> dict:
        schema = None
        if self.schema is None:
            self.schema = sql_conn.get_context()
        if use_db_schema:
            schema = self.schema
        prompt = self.pre_exec_prompt(human_query, schema)
        model_response = self.query_model(prompt)
        try:
            return self.parse_generic(model_response.content)
        except Exception as e:
            raise SqlAgentResponseParserError() from e

    def analyze_response(self, query: str, query_result: str, language: str) -> str:
        prompt = self.post_exec_prompt(query, query_result, language)

        return self.query_model(prompt)

    def invoke(self, query: str, db_config = None) -> tuple[str, str | None]:
        print(f'Starting with prompt: {query}')
        sql_conn = self.get_sql_connect()

        try:
            sql_query = self.translate_to_sql(sql_conn=sql_conn, human_query=query)
            if 'error' in sql_query:
                return sql_query['message'], None

            print(f"SQL Query: {sql_query['sql']}")
            results = sql_conn.run(sql_query['sql'])
            response = self.analyze_response(query, results, sql_query['language'])

            return ' '.join(response.content.split()), sql_query.get('sql')
        except Exception as e:
            raise SqlAgentUnexpectedError(f'Failed to invoke with: {e}') from e
