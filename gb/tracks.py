from flask import Flask, request, Response, jsonify, g

from gb import app, session
from gb.models import Track
from controllers import protected

@app.route('/api/tracks',methods=['GET'])
@protected
def get_all_tracks():
    user_id = g.current_user_id

    # look up all the tracks
    tracks = session.query(Track).filter_by(user_id=user_id).all()

    if not tracks:
        return jsonify(response="user {} has no tracks".format(user_id)),404

    return jsonify(tracks=[ track.to_json() for track in tracks])

@app.route('/api/tracks/<int:track_id>',methods=['GET'])
@protected
def get_one_track(track_id):
    user_id = g.current_user_id
    
    # get the track
    track = session.query(Track).get(track_id)

    # make sure the track was found
    if not track:
        return jsonify(response="Cannot fetch track {0} from user {1}".format(track_id,user_id)),404

    # make sure the track belongs to the userid
    if not track.user_id == int(user_id):
        return jsonify(response="Cannot return track {0} it does not belong to user {1}".format(track_id,user_id)),404

    # otherwise return it
    return jsonify(track.to_json())

@app.route('/api/tracks',methods=['POST'])
@protected
def new_track():
    user_id = g.current_user_id

    # Get json
    json = request.get_json()

    # Try and get everything
    track_name = json.get('track_name')
    data_type = json.get('data_type').lower()
    data_id = json.get('data_id')
    file_name = json.get('file_name')

    # Ensure everything was passed
    for field in [track_name,user_id,data_type,data_id,file_name]:
        if not field:
            return jsonify(response="Could not create track, {} field is required".format(track)),404

    new_track = Track(
        track_name = track_name,
        user_id = user_id,
        data_type = data_type,
        data_id = data_id,
        file_name = file_name,
    )

    session.add(new_track)
    session.commit()
    
    # Last check to make sure it was commited properly
    if not new_track.id:
        return jsonify(response="Could not create track"),404
    
    # Return the user id on success
    return jsonify(track_id=new_track.id)

@app.route('/api/tracks/<int:track_id>',methods=['PUT'])
@protected
def update_track(track_id):
    user_id = g.current_user_id

    if not track_id:
        return jsonify(response="Can't fetch track, track_id required"),404

    track = session.query(Track).get(track_id)
    json = request.get_json()

    if not track:
        return jsonify(response="Can't fetch track with id: {}".format(track_id)),404

    if not track.user_id == int(user_id):
        return jsonify(response="Cant update track {0} for user {1} they do not own it".format(track.id,user.id)),404

    for field in ['track_name','data_type','data_id']:
        val = json.get(field)
        if val:
            setattr(track,field,val)

    session.commit()
    return jsonify(track.to_json())

@app.route('/api/tracks/<int:track_id>',methods=['DELETE'])
@protected
def delete_track(track_id):
    user_id = g.current_user_id
    track = session.query(Track).get(track_id)

    if not track:
        return jsonify(response="Could not fetch track with id: {}".format(track_id)),404

    if not track.user_id == int(user_id):
        return jsonify(response="Could not delete track {0} it is not owned by user {1}".format(track.id,user_id)),404

    session.delete(track)
    session.commit()
    return jsonify()
