from flask import Flask, request, Response, jsonify
from angular_flask import app, db, session
from models import *
from controllers import check_headers
import pandas as pd

import pprint

@app.route('/api/files/',methods=['POST'])
@check_headers
def new_file():

    user_id = request.user_id
    file = request.files['file']
    type = request.form['type']

    if not file:
        return jsonify(response="Can't create upload file! No file found in form data"),404
    if not type in ['wig','bed','gtf','fasta']:
        return jsonify(response="Can't create upload file! {} is not a valid file type".format(type)),404
    
    if type == 'fasta':
        position = 0
        fasta_id = -1
        basepairs = []
        for line in file:
            if(line.startswith(">")):
            # Create a fasta and a wig data set, tracks, and a view holding them
                fasta = Fasta(header=line, file_name=file.filename)
                session.add(fasta)
                session.commit()
                fasta_id = fasta.id
            else:
                line.strip("\n")
                for base in line:
                    bp = BasePair(nucleotide=base,position=position,fasta_id=fasta_id)
                    position+=1
                    basepairs.append(bp)
        session.add_all(basepairs)
        session.commit()

        return jsonify(fasta_id = fasta_id)