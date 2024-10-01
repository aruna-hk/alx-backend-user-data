#!/usr/bin/python3
""" Basic authentication
"""

from api.v1.auth import Auth
import base64
from models.user import User
from models.base import *


class BasicAuth(Auth):
    """Basic Authentication"""

    def extract_base64_authorization_header(self, authorization_header: str)-> str:
        """extract username and password
        """
        if authorization_header and type(authorization_header) is str:
            auth_c = authorization_header.split(' ')
            if auth_c[0] == 'Basic':
                if len(auth_c) > 1:
                    return auth_c[1]
        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str)-> str:
        """decode authoriation header
        """
        if base64_authorization_header and type(base64_authorization_header) is str:
            try:
                return base64.b64decode(base64_authorization_header).decode("utf-8")
            except base64.binascii.Error:
                return None
        return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str)-> (str, str):
        """exctract credantials
        """
        if decoded_base64_authorization_header and type(decoded_base64_authorization_header) is str:
            credentials = decoded_base64_authorization_header.split(":")
            if len(credentials) != 2:
                return (None, None)
            return (credentials[0], credentials[1])
        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """return user object
        """
        if not user_email or type(user_email) is not str or not user_pwd or type(user_pwd) is not str:
            return None
        user = User.search({"email": user_email})
        if len(user) == 0:
            return None
        for _user in user:
            if _user.is_valid_password(user_pwd):
               return _user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return current/active user
        """
        auth_h = self.authorization_header(request)
        auth_header = self.extract_base64_authorization_header(self.authorization_header(request))
        credentials = self.extract_user_credentials(self.decode_base64_authorization_header(auth_header))
        return self.user_object_from_credentials(credentials[0], credentials[1])
