#!/usr/bin/env python3
"""class basic auth"""
from .auth import Auth
from base64 import b64encode, b64decode
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """class BasicAuth"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication:"""

        if (
            authorization_header is None
            or type(authorization_header) is not str
            or not authorization_header.startswith("Basic ")
        ):
            return None
        else:
            encoded = authorization_header.split(" ", 1)[1]
            return encoded

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """returns the decoded value of a Base64 string"""

        if (
            base64_authorization_header is None
            or type(base64_authorization_header) is not str
        ):
            return None
        try:
            return b64decode(base64_authorization_header).decode()
        except (TypeError, binascii.Error):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value."""
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) is not str
            or decoded_base64_authorization_header.find(":") == -1
        ):
            return (None, None)
        else:

            email = decoded_base64_authorization_header.split(":", 1)[0]
            password = decoded_base64_authorization_header.split(":")[1]

            return (email, password)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """returns the User instance based on his email and password."""
        if (
            not isinstance(user_email, str)
            or user_email is None
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None

        try:
            user_found = User.search({"email": user_email})

        except Exception:
            return None

        for user in user_found:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_auth_header)
        user_email, user_password = self.extract_user_credentials(decoded_header)
        user_extracted = self.user_object_from_credentials(user_email, user_password)
        return user_extracted
