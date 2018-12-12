#encoding: utf-8

from functools import wraps
from flask import session, redirect, url_for

# login
def login_xrequired(func):
    @wraps(func)
    def qingwa(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('home.login'))

    return qingwa
