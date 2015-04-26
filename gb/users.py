from flask import Flask, request, Response, jsonify
from flask_jwt import verify_jwt
from flask.ext.jwt import current_user

from gb import app, session
from gb.models import User

@app.route('/api/users/',methods=['GET'])
def get_user():
    verify_jwt()

    user_id = current_user.id
    user = session.query(User).get(user_id)

    if user:
        return jsonify( username=user.username, user_id=user.id, email=user.email )
    else:
        return jsonify(response="Can't fetch user with id: {}".format(user_id)),404

@app.route('/api/users',methods=['POST'])
def new_user():

    # Parse the json
    json = request.get_json()
    u_name = json.get('username')
    email = json.get('email')
    password = json.get('password')
    
    # Ensure username and email were passed
    if not u_name:
        return jsonify(response="Could not create user, username field is required"), 404
    elif u_name == "default":
        return jsonify(response="Invalid username."), 400

    if not email:
        return jsonify(response="Could not create user. email field is required"),404

    # Create user and commit
    new_user = User(username=json.get('username'),email=json.get('email'),password=json.get('password'))
    session.add(new_user)
    session.commit()
    
    # Last check to make sure it was commited properly
    if not new_user.id:
        return jsonify(response="Could not create user"),404
    
    # Return the user id on success
    return jsonify(user_id=new_user.id)

@app.route('/api/users/',methods=['PUT'])
def update_user():
    verify_jwt()

    user_id = current_user.id
    json = request.get_json()
    user = session.query(User).get(user_id)

    if not user:
        return jsonify(response="Can't fetch user with id: "+user_id),404

    if json.get('username'):
        user.username = json.get('username')

    if json.get('email'):
        user.email = json.get('email')
    
    session.commit()
    return jsonify(username=user.username, user_id=user.id, email=user.email)

@app.route('/api/users/',methods=['DELETE'])
def delete_user():
    verify_jwt()

    user_id = current_user.id
    user = session.query(User).get(user_id)

    if not user:
        return jsonify(response="Could not fetch user with id: "+user_id),404

    session.delete(user)
    session.commit()
    return jsonify()
