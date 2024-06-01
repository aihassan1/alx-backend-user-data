#!/usr/bin/env python3
"""
    Password Hashing Using Bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """expects one string argument name password
    returns a salted, hashed password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
