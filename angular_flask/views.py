from flask import Flask, request, Response, jsonify
from angular_flask import app, db, session
from models import *

@app.route('/views/<int:view_id>',methods=['GET'])
def get_view(view_id):

    # mock the user
    new_user = User(user_name="kyle",email="kyle@email.com")
    session.add(new_user)
    session.commit()


    # Mock the data
    fasta = Fasta(header=">Test Fasta Header")
    session.add(fasta)
    session.commit()

    i = 0
    for base in "ATTATTAGCATGCATGATCAGTAGCTAGGGGATGCATGCAACTGATCGATCGATGCATGCAT":
        bp = BasePair(nucleotide=base,position=i,fasta_id=fasta.id)
        i = i + 1
        session.add(bp)

    session.commit()

    # Mock the track
    track = Track(
        track_name = "Test Track",
        user_id = new_user.id,
        data_type = "fasta",
        data_id = fasta.id,
        file_name = "testFasta.fasta",
    )

    session.add(track)
    session.commit()

    view = View(view_name = "Test View")


    # Mock the view track
    view_trac = ViewTrack(track_id = track.id, view_id = view.id)

    print view
    return view