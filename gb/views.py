from flask import Flask, request, Response, jsonify
from gb import app, db, session
from models import *
from controllers import check_headers

@app.route('/api/views/',methods=['POST'])
@check_headers
def new_view():

    user_id = request.user_id
    json = request.get_json()

    track_ids = json.get('track_ids')
    view_name  = json.get('view_name')

    for field in [track_ids, view_name]:
    	if not field:
    		return jsonify(response="Could not create view, {} is required".format(field)),404

    new_view = View(view_name = view_name, user_id = user_id)
    session.add(new_view)
    session.commit()


    view_tracks = []
    for track_id in track_ids:
    	track = session.query(Track).get(track_id)
        if not track:
    		return jsonify(response="Could not create view, {} is not a valid track id".format(track_id)),404

    	if not track.user_id == int(user_id):
    		return jsonify(response="Could not create view with track {} is not a owned by user {}".format(track_id,user_id)),404

    	view_track = ViewTrack(track_id = track_id, view_id = new_view.id)
    	view_tracks.append(view_track)

    session.add_all(view_tracks)
    session.commit()
    return jsonify(new_view.to_json()),200

@app.route('/api/views/<int:view_id>',methods=['GET'])
@check_headers
def get_view(view_id):

    user_id = request.user_id

    view = session.query(View).get(view_id)

    # make sure the view was found
    if not view:
        return jsonify(response="Cannot fetch view {0} from user {1}".format(view_id,user_id)),404

    # make sure the view belongs to the userid
    if not view.user_id == int(user_id):
        return jsonify(response="Cannot return view {0} it does not belong to user {1}".format(view_id,user_id)),404

    # otherwise return it
    return jsonify(view.to_json())

@app.route('/api/views/',methods=['GET'])
@check_headers
def get_views():

    user_id = request.user_id

    views = session.query(View).filter_by(user_id=user_id).all()

    # make sure the view was found
    if not views:
        return jsonify(response="Cannot fetch views {0} from user {1}".format(view_id,user_id)),404

    # otherwise return it
    return jsonify(views=[ view.to_json() for view in views])

@app.route('/api/views/<int:view_id>',methods=['PUT'])
@check_headers
def update_view(view_id):

    user_id = request.user_id
    json = request.get_json()

    view = session.query(View).get(view_id)
    json = request.get_json()

    if not view:
        return jsonify(response="Can't fetch view with id: {}".format(view_id)),404

    if not view.user_id == int(user_id):
        return jsonify(response="Cant update view {0} for user {1} they do not own it".format(view.id,user.id)),404

    for field in ['view_name','view_tracks']:
        val = json.get(field)
        if val:
            setattr(track,field,val)

    session.commit()
    return jsonify(view.to_json())

@app.route('/api/views/<int:view_id>',methods=['DELETE'])
@check_headers
def delete_view(view_id):

    user_id = request.user_id
    view = session.query(View).get(view_id)

    if not view:
        return jsonify(response="Could not fetch view with id: {}".format(view_id)),404

    if not view.user_id == int(user_id):
        return jsonify(response="Could not delete view {0} it is not owned by user {1}".format(view.id,user_id)),404

    session.delete(view)
    session.commit()
    return jsonify()
