from flask import Flask, request, Response, jsonify, g
from gb import app, auth, db, session
from models import *
import re

@app.route('/api/files',methods=['POST'])
@auth.login_required
def new_file():
    user_id = g.user.id
    file = request.files['file']
    type = request.form['type']
    track_name = request.form['track_name'] if request.form.has_key('track_name') else file.filename

    if not file:
        return jsonify(response="Can't create upload file! No file found in form data"),404
    if not type in ['wig','bed','gtf','fasta']:
        return jsonify(response="Can't create upload file! {} is not a valid file type".format(type)),404

    if type == 'fasta':
        fasta_id = new_fasta(file)
        new_track = Track(
            track_name = track_name,
            user_id = user_id,
            data_type = type,
            data_id = fasta_id,
            file_name = file.filename,
        )
        session.add(new_track)
        session.commit()

        return jsonify(track_id = new_track.id)
    
    elif type == 'wig':
        wig_ids = new_wigs(file)
        new_tracks = []
        count = 1
        for wig_id in wig_ids:
            curr_name = "{}-{}".format(track_name, count)
            count += 1

            new_track = Track(
                track_name =  curr_name,
                user_id = user_id,
                data_type = type,
                data_id = wig_id,
                file_name = file.filename,
            )

            new_tracks.append(new_track)
        session.add_all(new_tracks)
        session.commit()
        return jsonify(track_ids = [new_track.id for new_track in new_tracks])

    elif type == 'gtf':
        gtf_id = new_gtf(file)
        new_track = Track(
            track_name = track_name,
            user_id = user_id,
            data_type = type,
            data_id = gtf_id,
            file_name = file.filename,
        )
        session.add(new_track)
        session.commit()
        return jsonify(track_id = new_track.id)

    elif type == 'bed':
        bed_id = new_bed(file)
        new_track = Track(
            track_name = track_name,
            user_id = user_id,
            data_type = type,
            data_id = bed_id,
            file_name = file.filename,
        )
        session.add(new_track)
        session.commit()
        return jsonify(track_id = new_track.id)


def valid_wig_header(header):
    if header.startswith("fixedStep"):
        return re.match(r"^fixedStep\schrom=\w+\sstart=\d+\sstep=\d+(\sspan=\d+$|$)", header)
    elif header.startswith("variableStep"):
        return re.match(r"^variableStep\schrom=\w+(\sspan=\d+$|$)", header)
    else:
        return False

def validate_fasta_header(header):
    return re.match(r"^>.*$",header)

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

def new_fasta(fasta_file):
    position = 0
    basepairs = []

    header = fasta_file.readline()

    if not validate_fasta_header(header):
        return jsonify(response="Cannot upload fasta file {} is not a valid header".format(header)),404

    fasta = Fasta(header=header)
    session.add(fasta)
    session.commit()
    fasta_id = fasta.id
    
    for line in fasta_file:
        line.strip("\n")

        for base in line:
            bp = BasePair(nucleotide=base,position=position,fasta_id=fasta_id)
            position+=1
            basepairs.append(bp)

    session.add_all(basepairs)
    session.commit()

    return fasta_id

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
    return wig_ids
    
def new_gtf(gtf_file):
    gtf_fields = ['seqname','source','feature','start','end','score','strand','frame','attribute']

    # create the base record
    gtf = Gtf()
    session.add(gtf)
    session.commit()

    gtf_values = []
    for line in gtf_file:

        gtf_dict = dict(zip(gtf_fields, line.split("\t")))
        gtf_dict['gtf_id'] = gtf.id

        # handle the '.' in score and frame
        if gtf_dict['score'] == '.':
            gtf_dict['score'] = 0.0
        if gtf_dict['frame'] == '.':
            gtf_dict['frame'] = 0

        # create each value record
        gtf_val = GtfValue(
            seqname = gtf_dict['seqname'],
            source = gtf_dict['source'],
            feature = gtf_dict['feature'],
            start = int(gtf_dict['start']),
            end = int(gtf_dict['end']),
            score = gtf_dict['score'],
            strand = gtf_dict['strand'],
            frame = int(gtf_dict['frame']),
            attribute = gtf_dict['attribute'],
            gtf_id = gtf_dict['gtf_id']
        )
        gtf_values.append(gtf_val)

    session.add_all(gtf_values)
    session.commit()
    return gtf.id

def new_bed(bed_file):

    # create the base record
    bed = Bed()
    session.add(bed)
    session.commit()

    bed_vals = []
    for line in bed_file:
        
        # skip the header
        if line.startswith("#"):
            continue

        line_vals = line.split("\t")

        if len(line_vals) != 12:
            app.logger.warning('Invalid bed line - skipping')
            continue

        [chrom, start, stop, name, score, strand, thick_start, 
        thick_end, item_rgb, block_count, bed_block_sizes, 
        bed_block_starts] = line_vals

        bed_val = BedValue(chrom, int(start), int(stop), name, int(score), strand, int(thick_start), int(thick_end), int(item_rgb), int(block_count), bed.id)
        session.add(bed_val)
        session.commit()

        index = 0
        bed_block_sizes = bed_block_sizes.rstrip(",").split(",")
        for size in bed_block_sizes:
            bed_block_size = BedBlockSize(index, size, bed_val.id)
            index += 1
            bed_vals.append(bed_block_size)

        index = 0
        bed_block_starts = bed_block_starts.rstrip("\n").split(",")
        for start in bed_block_starts:
            bed_block_start = BedBlockStart(index, start, bed_val.id)
            index += 1
            bed_vals.append(bed_block_start)

    session.add_all(bed_vals)
    session.commit()
    return bed.id
