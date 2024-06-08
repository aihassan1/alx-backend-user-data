#!/usr/bin/env python3
"""class session auth"""
from .auth import Auth
from uuid import uuid4
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, make_response
from os import getenv


class SessionAuth(Auth):
    """new authentication mechanism"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create a new session for a user
        returns the sessions id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_path():
    """login using email and password"""
    email = request.form.get("email")
    if email is None:
        return {"error": "email missing"}, 400
    password = request.form.get("password")
    if password is None:
        return {"error": "password missing"}, 400

    # try:
    #     user_ = User.search({"email": email})
    # except Exception:
    #     return {"error": "no user found for this email"}, 404
    
    user_ = User.search({"email": email})
    
    if not user_:
        return {"error": "no user found for this email"}, 404
    
    # If the password is not the one of the User found, return the JSON
    user = user_[0]
    
    if user.is_valid_password(password) is False:
        return {"error": "wrong password"}, 401

    else:
        from api.v1.app import auth

        session_id = auth.create_session(user.id)
        session_name = getenv("SESSION_NAME")
        response = make_response(user.to_json())
        response.set_cookie(session_name, session_id)
        return response

