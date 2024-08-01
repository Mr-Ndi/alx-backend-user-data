import os
import logging
from re import sub
import mysql.connector

# Define PII_FIELDS as a tuple of strings
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields, redaction, message, separator):
    """
    In this function we will have the following
    Arguments:

    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be
            obfuscated
    message: a string representing the log line
    separator: a string representing by which character
            is separating all fields in the log line (message)
    """
    pattern = '|'.join([f'{field}=.+?{separator}' for field in fields])
    return sub(pattern,
               lambda match: f"{match.group().split('=')[0]}={redaction}{separator}",
               message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields,
        self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)

def get_db():
    """
    Returns a connector to the MySQL database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
    
    return connection

def main():
    """
    Main function that retrieves and displays user data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    
    for row in cursor:
        # Create a log message with the user data
        log_message = f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]};"
        logger.info(log_message)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
