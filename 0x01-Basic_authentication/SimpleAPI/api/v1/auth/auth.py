""" Authentication class module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication classs
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if auth required
        """

        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if path.endswith('/'):
            if path[:-1] in excluded_paths:
                return False
        else:
            if path + "/" in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """get authorization header"""

        if request:
            if request.authorization:
                return str(request.authorization)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return current logged user obj
        """

        return None
