from flask import Flask, request, Response, jsonify
from gb import app, db, session
from models import *
from controllers import check_headers
import pandas as pd
import re
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
        return new_fasta(file)
    
    elif type == 'wig':
        return new_wigs(file)
        
def valid_wig_header(header):
    if header.startswith("fixedStep"):
        return re.match(r"^fixedStep\schrom=\w+\sstart=\d+\sstep=\d+(\sspan=\d+$|$)", header)
    elif header.startswith("variableStep"):
        return re.match(r"^variableStep\schrom=\w+(\sspan=\d+$|$)", header)
    else:
        return False

def parse_header(header):
    array = header.split()
    step_type = array.pop(0)
    
    # set the values
    values = dict(item.split("=") for item in array)
    values['stepType'] = step_type
    
    # convert the stuff to int
    for int_key in ["start","step","span"]:
        if int_key in values:
            values[int_key] = int(values[int_key])

    return values

# TODO implement support for multi fasta files
def new_fasta(fasta_file):
    position = 0
    fasta_id = -1
    basepairs = []
    for line in fasta_file:
        if(line.startswith(">")):
        # Create a fasta and a wig data set, tracks, and a view holding them
            fasta = Fasta(header=line)
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

    return jsonify(fasta_id = fasta_id),200


def new_wigs(wig_file):
    current_id = -1
    current_dict = None
    current_data = []
    wig_ids = []
        
    for line in wig_file:
        if line.startswith("track"):
            continue
        
        # this line starts a wig block
        elif line.startswith("variableStep") or line.startswith("fixedStep"):
            # validate the wig header is valid 
            if not valid_wig_header(line):
                return jsonify(response="Wig format incorrect"),404

            # get the values from the header
            header_dict = parse_header(line)

            # commit the bases from the the previous wig
            if current_data:
                session.add_all(current_data)
                session.commit()

            # create the new wig
            wig = Wig(chrom=header_dict['chrom'])
            session.add(wig)
            session.commit()
            current_id = wig.id
            wig_ids.append(current_id)
            current_dict = header_dict
            current_data = []
        
        # we have a data line
        else:

            # parse a var step line
            if current_dict['stepType'] == "variableStep":
                (position, score) = (int(val) for val in line.split())
                
                # if there is no span it is easy
                if 'span' not in current_dict:
                    wig_val = WigValue(
                        position = position,
                        value = score,
                        wig_id = current_id
                    )
                    current_data.append(wig_val)

                # handle the span
                else:
                    span = int(current_dict['span'])
                    for pos in range(position, position+span):
                        wig_val = WigValue(
                            position = pos,
                            value = score,
                            wig_id = current_id
                        )
                        current_data.append(wig_val)

            # parse a fix step line
            else:
                score = int(line.strip()) 
                # if there is no span it is easy
                if 'span' not in current_dict:
                    wig_val = WigValue(
                        position = current_dict['start'],
                        value = score,
                        wig_id = current_id
                    )
                    current_data.append(wig_val)
                    current_dict['start'] += current_dict['step']
                                    # handle the span
                else:
                    span = current_dict['span']
                    for pos in range(current_dict['start'], current_dict['start']+span):
                        wig_val = WigValue(
                            position = pos,
                            value = score,
                            wig_id = current_id
                        )
                        current_data.append(wig_val)
                    current_dict['start'] += current_dict['step']
    session.add_all(current_data)
    session.commit()
    return jsonify(wig_ids = wig_ids),200
