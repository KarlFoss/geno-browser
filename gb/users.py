from flask import Flask, request, Response, jsonify
from gb import app, db, session
from gb.models import User
from controllers import check_headers

@app.route('/api/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user = session.query(User).get(user_id)
    if(user):
        return jsonify( user_name=user.user_name, user_id=user.id, email=user.email)
    else:
        return jsonify(response="Can't fetch user with id: {}".format(user_id)),404

@app.route('/api/users',methods=['POST'])
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

@app.route('/api/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    json = request.get_json()
    user = session.query(User).get(user_id)

    if not user:
        return jsonify(response="Can't fetch user with id: "+user_id),404

    if json.get('user_name'):
        user.user_name = json.get('user_name')

    if json.get('email'):
        user.email = json.get('email')
    
    session.commit()
    return jsonify(user_name=user.user_name, user_id=user.id, email=user.email)

@app.route('/api/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = session.query(User).get(user_id)

    if not user:
        return jsonify(response="Could not fetch user with id: "+user_id),404

    session.delete(user)
    session.commit()
    return jsonify()
