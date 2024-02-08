#!/usr/bin/env python3
"""this docs contains class and functions to Definition of
filter_datum function that returns an obfuscated log message
"""
import os
import re
import logging
import mysql.connector
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """this func to obfuscated log message
    args:
        fields: to list of strings indicating fields to obfuscate
        redaction: the field will be obfuscated to
        message: log line to obfuscate
        separator: character separating the fields
    return:
        the result of log message
    """
    for fd in fields:
        message = re.sub(fd+'=.*?'+separator, fd+'='+redaction+separator,
                         message)

    return message


class RedactingFormatter(logging.Formatter):
    """this class is to Redacting Formatter class
        this class is to Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """this func to initialize the list"""
        super(RedactingFormatter, self).__init__(self.FORMAT)

        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """this function to redact the message of LogRecord instance
        args:
            record: the LogRecord instance containing message
        return:
            to return the result formatted string
        """
        message = super(RedactingFormatter, self).format(record)

        redactx = filter_datum(self.fields, self.REDACTION, message,
                               self.SEPARATOR)
        return redactx


def get_logger() -> logging.Logger:
    """this function to Return a logging.Logger object"""
    logx = logging.getLogger("user_data")

    logx.setLevel(logging.INFO)
    logx.propagate = False

    handx = logging.StreamHandler()
    formatx = RedactingFormatter(PII_FIELDS)

    handx.setFormatter(formatx)
    logx.addHandler(handx)

    return logx


def get_db() -> mysql.connector.connection.MySQLConnection:
    """this func to connect to mysql and we will be using
        many of paramteres right now.
    """
    us = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    pas = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""

    hos = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_nam = os.getenv('PERSONAL_DATA_DB_NAME')

    conct = mysql.connector.connect(user=us, password=pas,
                                    host=hos, database=db_nam)
    return conct


def main():
    """this function its name is main
        and it aims to entry point
    """
    db = get_db()
    logx = get_logger()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    fields = cursor.column_names

    for rw in cursor:
        meg = "".join("{}={}; ".format(k, vl) for k, vl in zip(fields, rw))
        logx.info(meg.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
