#!/usr/bin/env python3
"""new flask APP"""

from flask import jsonify, Flask, request, json, abort, make_response
from flask import redirect, url_for
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


@app.route(rule="/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """logs out a user and destroy its session"""
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """returns a user profile based on session id"""
    session_id_cookie = request.cookies.get("session_id", None)
    if session_id_cookie is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id_cookie)
    if user is None:
        abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """get_reset_password_token"""
    email = request.form.get("email")
    try:
        reset_pwd_token = AUTH.get_reset_password_token(email)
        response = make_response(
            jsonify({"email": email, "reset_token": reset_pwd_token})
        )
        return response, 200
    except ValueError:
        abort(403)


@app.route(rule="/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """update the password"""
    email = request.form.get("email")
    password = request.form.get("password")
    reset_token = request.form.get("reset_token")

    try:
        AUTH.update_password(reset_token, password)
    except Exception:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
