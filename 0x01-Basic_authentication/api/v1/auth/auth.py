#!/usr/bin/env python3
"""class auth"""

from flask import request
from typing import List, TypeVar


class Auth:
    """class auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        if request is None:
            return None


        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """current_user"""
        return None
