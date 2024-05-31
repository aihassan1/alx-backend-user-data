#!/usr/bin/env python3
"""
this module contains user data management
"""
from typing import List
import logging
import mysql.connector
import os
import re


PII_FIELDS = ("name", "password", "phone", "ssn", "email")


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

    def __init__(self, fields: List[str]):
        """initialization method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """this function filters values in incoming log records using
        filter_datum function"""
        return filter_datum(
            self.fields,
            self.REDACTION,
            super(RedactingFormatter, self).format(record),
            self.SEPARATOR,
        )


def get_logger() -> logging.Logger:
    """this method returns a user data logger"""
    logger = logging.getLogger("user_data")

    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """get_db function that returns a connector to the database"""
    connection = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
    )
    return connection


def main() -> None:
    """function will obtain a database connection
    using get_db and retrieve all rows in the users
    table and display each row under a filtered format"""
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    logger = get_logger()

    for row in rows:
        formatted_row = f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]};"
        logger.info(formatted_row)

    db_connection.close()


if __name__ == "__main__":
    main()
