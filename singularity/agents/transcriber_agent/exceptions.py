class TranscriberError(Exception):
    """Transcriber Error"""


class TranscriberParserError(TranscriberError):
    """Transcriber Parser"""


class TranscriberFileNotFoundError(TranscriberError):
    """Transcriber File Not Found Error"""
