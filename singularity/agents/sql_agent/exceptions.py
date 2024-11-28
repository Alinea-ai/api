class SqlAgentError(Exception):
    """SqlAgent Error"""


class SqlAgentConnectionError(SqlAgentError):
    """SqlAgent Connection Error"""


class SqlAgentTimeoutError(SqlAgentError):
    """SqlAgent Timeout Error"""


class SqlAgentUnexpectedError(SqlAgentError):
    """SqlAgent Unexpected"""


class SqlAgentResponseParserError(SqlAgentError):
    """SqlAgent Response"""
