#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User
from typing import Dict, Any

from user import Base


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds a new user to the db
        returns a new user object"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """
        Search for a user in the database based on the provided keyword args

        Args:
            **kwargs: Keyword arguments representing the search criteria.

        Returns:
            The User object that matches the search criteria.

        Raises:
            InvalidRequestError: if the keys in the dict are invalid
            NoResultFound: If no user is found
        """
        keys = list(kwargs.keys())

        for key in keys:
            if not hasattr(User, key):
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """update a user"""
        if kwargs:
            try:
                user = self.find_user_by(id=user_id)
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                    else:
                        raise ValueError
                self._session.commit()
            except NoResultFound:
                pass
            return None
