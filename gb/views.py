from flask import Flask, request, Response, jsonify
from gb import app, db, session
from models import *
from controllers import check_headers

@app.route('/api/views/',methods=['POST'])
@check_headers
def new_view(view_id):

    user_id = request.user_id

@app.route('/api/views/<int:view_id>',methods=['GET'])
@check_headers
def get_view(view_id):

    user_id = request.user_id


@app.route('/api/views/<int:view_id>',methods=['PUT'])
@check_headers
def update_view(view_id):

    user_id = request.user_id


@app.route('/api/views/<int:view_id>',methods=['DELETE'])
@check_headers
def delete_view(view_id):

    user_id = request.user_id
