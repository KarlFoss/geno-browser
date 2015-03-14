import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory, jsonify
from flask import send_file, make_response, abort

from angular_flask import parse_data

from angular_flask import app
from angular_flask import db

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

#@app.route('/<model_name>/')
#@app.route('/<model_name>/<item_id>')
@app.route('/users/<user_id>',methods=['GET','POST','PUT','DELETE'])
def user(user_id):
    if request.method == 'GET':
        user = db.session.query(User).get(user_id)
        if(user):
            return jsonify( user_name=user.user_name, user_id=user.id, email=user.email)
        else:
            return jsonify(message="Can't fetch user with id: "+user_id),404
#    elif request.method == 'POST':
#        json = request.get_json()
#        print json
#        return json
#    elif request.method == 'PUT':
#    	
#    elif request.method == 'DELETE':
#    	#
#    else
#    	#
## special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



