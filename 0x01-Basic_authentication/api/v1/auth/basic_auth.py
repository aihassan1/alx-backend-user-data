#!/usr/bin/env python3
"""class basic auth"""
from .auth import Auth
from base64 import b64encode


class BasicAuth(Auth):
    """class BasicAuth"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication:"""

        if (
            authorization_header is None
            or type(authorization_header) is not str
            or authorization_header.startswith("Basic ")
        ):
            return None
        else:
            return b64encode(authorization_header.encode()).decode()
