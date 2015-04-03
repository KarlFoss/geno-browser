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

    	#if not track.user_id == user_id:
    	#	return jsonify(response="Could not create view with track {} is not a owned by user {}".format(track_id,user_id)),404

    	view_track = ViewTrack(track_id = track_id, view_id = new_view.id)
    	view_tracks.append(view_track)

    session.add_all(view_tracks)
    session.commit()
    return jsonify(new_view.to_json())

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
