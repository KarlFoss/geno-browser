from flask import Flask, request, Response, jsonify
from angular_flask import app, db, session
from models import *

@app.route('/views/',methods=['POST'])
def new_view(view_id):

     # get user_id
    user_id = request.headers.get("X-Userid")
    if not user_id:
        return jsonify(response="Can't create view for user, X-Userid header not set"),404

    # First make sure the user exists
    user = session.query(User).get(user_id)
    if not user:
        return jsonify(response="Can't create view for user with id: {} , user does not exists".format(user_id)),404

@app.route('/views/<int:view_id>',methods=['GET'])
def get_view(view_id):

     # get user_id
    user_id = request.headers.get("X-Userid")
    if not user_id:
        return jsonify(response="Can't fetch view for user, X-Userid header not set"),404

    # First make sure the user exists
    user = session.query(User).get(user_id)
    if not user:
        return jsonify(response="Can't fetch view for user with id: {} , user does not exists".format(user_id)),404

@app.route('/views/<int:view_id>',methods=['PUT'])
def update_view(view_id):

     # get user_id
    user_id = request.headers.get("X-Userid")
    if not user_id:
        return jsonify(response="Can't update view for user, X-Userid header not set"),404
    
    # First make sure the user exists
    user = session.query(User).get(user_id)
    if not user:
        return jsonify(response="Can't update view for user with id: {} , user does not exists".format(user_id)),404

@app.route('/views/<int:view_id>',methods=['DELETE'])
def delete_view(view_id):

     # get user_id
    user_id = request.headers.get("X-Userid")
    if not user_id:
        return jsonify(response="Can't delete view for user, X-Userid header not set"),404

    # First make sure the user exists
    user = session.query(User).get(user_id)
    if not user:
        return jsonify(response="Can't delete view for user with id: {} , user does not exists".format(user_id)),404