import os
from functools import wraps

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory, jsonify, g
from flask_jwt import verify_jwt
from flask.ext.jwt import current_user
from gb import jwt
from gb.models import *

class UserObj(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

@jwt.authentication_handler
def authenticate(username, password):
    user = User.query.filter_by(username = username).first()
    if user and user.verify_password(password):
        return UserObj(id=user.id, username=user.username)

@jwt.user_handler
def load_user(payload):
    user = User.query.filter_by(id = payload['user_id']).first()
    if user:
        return UserObj(id=user.id, username=user.username)

def protected(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # check if authorization header is set
        auth = request.headers.get('Authorization', None)

        # if it is, verify jwt
        if auth:
            verify_jwt()
            g.current_user_id = current_user.id

        # if not, use the default user
        else:
            user = session.query(User).filter_by(username="default").first()
            if user:
                g.current_user_id = user.id
            else:
                return jsonify(response="No default user defined!"), 401

        return func(*args, **kwargs)
    return decorated_function

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
def basic_pages(**kwargs):
    return app.send_static_file('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(response="Invalid Request"), 404

from gb import users, tracks, views, files