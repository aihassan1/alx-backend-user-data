#!/usr/bin/env python3
"""new flask APP"""

from flask import jsonify, Flask, request, json, abort, make_response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """this method registers new users -> POST /users"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})

    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> json:
    """login a user if email and password are correct"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(
        jsonify({"email": "f{email}", "message": "logged in"}))
    response.set_cookie(session_id, session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
