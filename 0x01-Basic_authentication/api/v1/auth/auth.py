#!/usr/bin/env python3
"""class auth"""

from flask import request
from typing import List, TypeVar


class Auth:
    """returns True if the path is not in the list
    of strings excluded_paths"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method"""

        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        path = path if path.endswith("/") else path + "/"

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        if request is None:
            return None
        if not request.get("Authorization"):
            return None
        else:
            return request.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """current_user"""
        return None
