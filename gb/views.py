from flask import Flask, request, Response, jsonify
from gb import app, db, session
from models import *
from controllers import check_headers

@app.route('/api/views/',methods=['POST'])
@check_headers
def new_view(view_id):

    user_id = request.user_id

    # First make sure the user exists
    user = session.query(User).get(user_id)
    if not user:
        return jsonify(response="Can't create view for user with id: {} , user does not exists".format(user_id)),404

@app.route('/api/views/<int:view_id>',methods=['GET'])
@check_headers
def get_view(view_id):

    user_id = request.user_id

    # First make sure the user exists
    user = session.query(User).get(user_id)
    if not user:
        return jsonify(response="Can't fetch view for user with id: {} , user does not exists".format(user_id)),404

@app.route('/api/views/<int:view_id>',methods=['PUT'])
@check_headers
def update_view(view_id):

    user_id = request.user_id

    # First make sure the user exists
    user = session.query(User).get(user_id)
    if not user:
        return jsonify(response="Can't update view for user with id: {} , user does not exists".format(user_id)),404

@app.route('/api/views/<int:view_id>',methods=['DELETE'])
@check_headers
def delete_view(view_id):

    user_id = request.user_id

    # First make sure the user exists
    user = session.query(User).get(user_id)
    if not user:
        return jsonify(response="Can't delete view for user with id: {} , user does not exists".format(user_id)),404