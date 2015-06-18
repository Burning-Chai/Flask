# -*- coding: utf-8 -*-

from functools import wraps
from flask import request, Response

BASIC_AUTH_USERNAME = '<username>'
BASIC_AUTH_PASSWORD = '<password>'


def check_auth(username, password):
    """
    This function is called to check if a username / password combination is valid.
    """

    return username == BASIC_AUTH_USERNAME and password == BASIC_AUTH_PASSWORD


def authenticate():
    """
    Sends a 401 response that enables basic auth
    """

    return Response(
        'Could not verify your access level for that URL.<br>You have to login with proper credentials',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
