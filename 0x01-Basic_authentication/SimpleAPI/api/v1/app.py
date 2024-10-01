#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth import BasicAuth
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == "auth":
    from api.v1.auth import Auth
    auth = Auth()

exclude_list = [
    '/api/v1/status/',
    '/api/v1/unauthorized/',
    '/api/v1/forbidden/'
]


@app.before_request
def before_request():
    print("before request")
    if auth:
        if auth.require_auth(request.path, exclude_list):
            auth_header = auth.authorization_header(request)
            if not auth_header:
                abort(401)
            current_user = auth.current_user(request)
            print("----", current_user)
            if not current_user:
                abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
