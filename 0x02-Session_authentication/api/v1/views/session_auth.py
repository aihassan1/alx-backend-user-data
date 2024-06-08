#!/usr/bin/env python3
"""view session auth"""

from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, make_response
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_path():
    """login using email and password"""
    email = request.form.get("email")
    if email is None:
        return {"error": "email missing"}, 400
    password = request.form.get("password")
    if password is None:
        return {"error": "password missing"}, 400

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
