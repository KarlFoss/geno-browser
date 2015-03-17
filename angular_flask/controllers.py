import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory, jsonify
from flask import send_file, make_response, abort

from angular_flask import parse_data
from angular_flask import app, db, session

# routing for API endpoints (generated from the models designated as API_MODELS)
from angular_flask.models import *

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/about')
@app.route('/blog')
def basic_pages(**kwargs):
	return make_response(open('angular_flask/templates/index.html').read())

@app.route('/gene_test',methods=['GET','POST'])
def gene():
    if request.method == 'GET':
        return 'ADFS'
    else:
        f = request.files['file']
        return str(parse_data.parse_file(f).shape)

@app.route('/users/',methods=['POST'])
def new_user():
    # Parse the json
    json = request.get_json()
    u_name = json.get('user_name')
    email = json.get('email')
    
    # Ensure user_name and email were passed
    if not u_name:
        return jsonify(response="Could not create user, user_name field is required"),404

    if not email:
        return jsonify(response="Could not create user. email field is required"),404

    # Crete user and commit 
    new_user = User(user_name=json.get('user_name'),email=json.get('email'))
    session.add(new_user)
    session.commit()
    
    # Last check to make sure it was commited properly
    if not new_user.id:
        return jsonify(response="Could not create user"),404
    
    # Return the user id on success
    return jsonify(user_id=new_user.id)

@app.route('/users/<user_id>',methods=['GET'])
def get_user(user_id):
    user = session.query(User).get(user_id)
    if(user):
        return jsonify( user_name=user.user_name, user_id=user.id, email=user.email)
    else:
        return jsonify(response="Can't fetch user with id: "+user_id),404

@app.route('/users/<user_id>',methods=['PUT'])
def update_user(user_id):
    json = request.get_json()
    user = session.query(User).get(user_id)

    # Set all fields
    if json.get('user_name'):
        user.user_name = json.get('user_name')

    if json.get('email'):
        user.email = json.get('email')

    session.commit()
    return jsonify(user_name=user.user_name)


## special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



