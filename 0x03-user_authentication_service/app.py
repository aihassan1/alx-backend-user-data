#!/usr/bin/env python3
"""new flask APP"""

from flask import jsonify, Flask, render_template, make_response, request, Response
from auth import Auth
from sqlalchemy.exc import u

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """home page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["post"])
def add_user():
    """adds a new user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        AUTH.register_user(email, password)
        return {"email": f"{email}", "message": "user created"}
    except Exception:
        return ({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
