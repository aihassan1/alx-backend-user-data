#!/usr/bin/env python3
"""auth module"""
from bcrypt import gensalt, hashpw


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returns bytes."""
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)
    return hashed_password
