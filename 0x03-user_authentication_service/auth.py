#!/usr/bin/env python3
"""auth module"""
from bcrypt import gensalt, hashpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import checkpw
from uuid import uuid4, UUID


def _hash_password(password: str) -> bytes:
    """method that takes in a password string arguments and returns bytes."""
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """CREATE A NEW USER
        if a user exists raise value err User <user's email> already exists
        returns : the user object
        """
        # check if the user already exists
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """expects email and password required arguments
        returns a boolean"""
        if email is None or password is None:
            return False

        try:
            user_found = self._db.find_user_by(email=email)
            if user_found is not None:
                user_hashed_password = user_found.hashed_password
                return checkpw(password.encode(), user_hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """takes an email string argument and returns the session ID"""
        try:
            current_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(current_user.id, session_id=session_id)
            return session_id

        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """takes a single session_id string argument
        returns the corresponding User or None."""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user

        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user session ID to None."""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """returns a reset token if the user exists"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = uuid4()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError
