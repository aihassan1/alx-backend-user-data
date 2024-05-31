#!/usr/bin/env python3
"""Write a function called filter_datum that returns the log message obfuscated:"""
import re, logging
from typing import List, Logger


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns a log message obfuscated"""
    for field in fields:
        message = re.sub(
            f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    # Update the class to accept a list of strings fields constructor argument.
    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format func"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


def get_logger() -> Logger:
    
