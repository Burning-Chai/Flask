#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from decorator import requires_auth

app = Flask(__name__)

@app.before_request
@requires_auth
def before_request():
    pass

@app.route("/")
def index():
    return "Hello World!"

@app.route("/hello")
def hello():
    return "Hello Hello Hello Hello"

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True, ssl_context=(
        '<server.keyのディレクトリ>/server.crt',
        '<server.keyのディレクトリ>/server.key'
    ))
