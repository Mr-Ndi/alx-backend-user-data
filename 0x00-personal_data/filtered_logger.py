#!/usr/bin/env python3

"""
    A module that contains functions like filter_datum
"""
import os
import logging
from re import sub
import mysql.connector

# Define PII_FIELDS as a tuple of strings
# PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields, redaction, message, separator):
    """
    In this function we will have the following
    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be.
    message: a string representing the log line
    separator: a that string represents
    """
    pattern = '|'.join([f'{field}=.+?{separator}' for field in fields])
    return sub(
        pattern,
        lambda match: f"{match.group().split('=')[0]}={redaction}{separator}",
        message
    )
