import os

from flask import render_template, url_for, redirect, send_from_directory, jsonify
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