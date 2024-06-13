#!/usr/bin/env python3
"""new flask APP"""

from flask import jsonify, request, Flask, render_template, make_response


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """home page"""
    return jsonify('{"message": "Bienvenue"}')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
