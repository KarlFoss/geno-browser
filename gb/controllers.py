import os
from functools import wraps

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory, jsonify
from flask import send_file, make_response, abort, g
from gb import app, db, session, parse_data
from gb.models import *

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
def basic_pages(**kwargs):
    return redirect('/static/index.html')

@app.route('/api/token', methods=["GET"])
def get_token():
    username = request.headers.get("username")
    password = request.headers.get("password")

    token = username #g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/static/index.html')

@auth.verify_password
def verify_password(token, password):
    user = User.verify_token(token)
    if not user:
        return False

    g.user_id = user.id
    return True

def check_headers(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):   
        # get user_id
        user_id = request.headers.get("X-Userid")

        if not user_id:
            return jsonify(response="Can't fetch tracks for user, X-UserId header not set"),404

        # First make sure the user exists
        user = session.query(User).get(user_id)
        if not user:
            return jsonify(response="Can't fetch tracks for user with id: {}".format(user_id)),404

        request.user_id = user_id

        return func(*args, **kwargs)
    return decorated_function

@app.route('/gene_test',methods=['GET','POST'])
def gene():
    if request.method == 'GET':
        return 'ADFS'
    else:
        f = request.files['file']
        return str(parse_data.parse_file(f).shape)

from gb import users,tracks,views,files
