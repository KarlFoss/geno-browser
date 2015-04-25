from flask import Flask, request, Response, jsonify, g
from gb import app, auth, db, session
from models import *

@app.route('/api/views/',methods=['POST'])
@auth.login_required
def new_view():
    user_id = g.user.id
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
    return jsonify(view_id=new_view.id),200

@app.route('/api/views/<int:view_id>',methods=['GET'])
@auth.login_required
def get_view(view_id):
    user_id = g.user.id
    view = session.query(View).get(view_id)

    # make sure the view was found
    if not view:
        return jsonify(response="Cannot fetch view {0} from user {1}".format(view_id,user_id)),404

    # make sure the view belongs to the userid
    if not view.user_id == int(user_id):
        return jsonify(response="Cannot return view {0} it does not belong to user {1}".format(view_id,user_id)),404

    # otherwise return it
    return jsonify(view.to_json())

@app.route('/api/views/data/<int:view_id>',methods=['GET'])
@auth.login_required
def get_data_view(view_id):
    user_id = g.user.id
    view = session.query(View).get(view_id)

    # make sure the view was found
    if not view:
        return jsonify(response="Cannot fetch view {0} from user {1}".format(view_id,user_id)),404

    # make sure the view belongs to the userid
    if not view.user_id == int(user_id):
        return jsonify(response="Cannot return view {0} it does not belong to user {1}".format(view_id,user_id)),404

    # otherwise return it
    return jsonify(view.to_data())

@app.route('/api/views/',methods=['GET'])
@auth.login_required
def get_views():
    user_id = g.user.id
    views = session.query(View).filter_by(user_id=user_id).all()

    # make sure the view was found
    if not views:
        return jsonify(response="Cannot fetch views from user {0}".format(user_id)),404

    # otherwise return it
    return jsonify(views=[ view.to_json() for view in views])

@app.route('/api/views/<int:view_id>',methods=['PUT'])
@auth.login_required
def update_view(view_id):
    user_id = g.user.id
    json = request.get_json()
    view = session.query(View).get(view_id)

    if not view:
        return jsonify(response="Can't fetch view with id: {}".format(view_id)),404

    if not view.user_id == int(user_id):
        return jsonify(response="Cant update view {0} for user {1} they do not own it".format(view.id,user.id)),404

    # update the view_name if given
    view_name = json.get('view_name')
    if view_name:
        view.view_name = view_name

    # update the viewtracks if given
    track_ids = json.get('track_ids')
    if track_ids is not None:
        track_ids = set(track_ids)
        existing_ids = set(view_track.track_id for view_track in view.view_tracks)
        for new_track_id in track_ids.difference(existing_ids):
            app.logger.warning('Adding track {}'.format(new_track_id))
            session.add(ViewTrack(track_id=new_track_id, view_id=view.id))
        for stale_track_id in existing_ids.difference(track_ids):
            app.logger.warning('Removing track {}'.format(stale_track_id))
            session.delete(session.query(ViewTrack).filter_by(track_id=stale_track_id,view_id=view.id).first())
        
        session.commit()
    return jsonify(view.to_json())

@app.route('/api/views/<int:view_id>',methods=['DELETE'])
@auth.login_required
def delete_view(view_id):
    user_id = g.user.id
    view = session.query(View).get(view_id)

    if not view:
        return jsonify(response="Could not fetch view with id: {}".format(view_id)),404

    if not view.user_id == int(user_id):
        return jsonify(response="Could not delete view {0} it is not owned by user {1}".format(view.id,user_id)),404

    session.delete(view)
    session.commit()
    return jsonify()