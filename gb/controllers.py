import os
from functools import wraps

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory, jsonify
from flask import send_file, make_response, abort, g
from gb import app, auth, db, session, parse_data
from gb.models import *

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

@app.route('/api/token', methods=["GET"])
@auth.login_required
def get_token():
    token = g.user.generate_token()
    return jsonify({ 'X-Access-Token': token.decode('ascii') })

@app.route('/gene_test',methods=['GET','POST'])
def gene():
    if request.method == 'GET':
        return 'ADFS'
    else:
        f = request.files['file']
        return str(parse_data.parse_file(f).shape)

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            user = User.query.filter_by(username="default").first()

    g.user = user
    return True

from gb import users,tracks,views,files
