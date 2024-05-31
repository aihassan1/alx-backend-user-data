#!/usr/bin/env python3
"""
    Password Hashing Using Bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Create new hashed password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Compare entered password with the stored password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
