#!/usr/bin/python3
"""
    Now we are about to create a module to manage
    the API authentication.
"""
from flask import request


class Auth:
    """
        Now we are about to create a class to manage
        the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            A function that checks if authantication is
            required to acces a path
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
            Some random comments
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Another random comments
        """
        return None
