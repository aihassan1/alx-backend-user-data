#!/usr/bin/env python3
"""Write a function called filter_datum that returns the log message obfuscated:"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(rf"{field}=([^;]*);", f"{field}={redaction};", message)
    return message
