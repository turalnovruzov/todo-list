from flask import session, redirect
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("uid") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
