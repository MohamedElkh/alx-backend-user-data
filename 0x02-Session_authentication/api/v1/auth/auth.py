#!/usr/bin/env python3
"""this model Definition of class Auth"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """class to Manages the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        Args:
            - path: this Url path to be checked
            - excluded_paths: this List of paths that do not require
        Return:
            True if path is not in excluded_paths
        """
        if path is None:
            return True

        elif excluded_paths is None or excluded_paths == []:
            return True

        elif path in excluded_paths:
            return False

        else:
            for x in excluded_paths:
                if x.startswith(path):
                    return False

                if path.startswith(x):
                    return False

                if x[-1] == "*":
                    if path.startswith(x[:-1]):
                        return False

        return True

    def authorization_header(self, request=None) -> str:
        """func to Returns the authorization header from a request"""
        if request is None:
            return None

        header = request.headers.get('Authorization')

        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """func Returns a User instance from information from"""
        return None

    def session_cookie(self, request=None):
        """
        func to Returns a cookie from a request
        Args:
            request : request object
        Return:
            value of _my_session_id cookie from request object
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')

        return request.cookies.get(session_name)
