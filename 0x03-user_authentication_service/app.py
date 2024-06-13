#!/usr/bin/env python3
"""new flask APP"""

from flask import jsonify, Flask, render_template, make_response, request, Response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["post"], strict_slashes=False)
def add_user() -> str:
    """adds a new user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = AUTH.register_user(email, password)
        if new_user is not None:
            return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
