#!/usr/bin/env python3
"""Write a function called filter_datum that returns the log message obfuscated:"""
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(
            rf"{field}=([^;]*){separator}", f"{field}={redaction};", message
        )
    return message
