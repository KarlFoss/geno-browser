import os
import json
import argparse
import requests
import random

from flask import g

from gb import app, db, session
from gb.models import BasePair
from gb.models import *

def create_sample_db_entry(api_endpoint, payload):
    url = 'http://localhost:5000/' + api_endpoint
    r = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print r.text
    
def create_db():
    db.create_all()

def drop_db():
    db.drop_all()

def seed_db():

    # Setup default user #
    default_user = User(username="default", email="default@gb.com", password="default")
    session.add(default_user)
    session.commit()

    # add the users
    user_ids = [default_user.id]
    users = ["kyle","karl","coda","max","goof"]
    for name in users:
        new_user = User(username=name,email="{}@email.com".format(name),password="SECRET")
        session.add(new_user)
        session.commit()
        user_ids.append(new_user.id)

    ## Give each a track ##
    for u_id in user_ids:

        view = View(view_name = "Test View", user_id = u_id)
        session.add(view)
        session.commit()

        # Create a fasta
        fasta = Fasta(header=">EBV1")
        session.add(fasta)
        session.commit()

        i = 0
        for base in "ATTATTAGCATGCATGATCAGTAGCTAGGGGATGCATGCAACTGATCGATCGATGCATGCAT":
            bp = BasePair(nucleotide=base,position=i,fasta_id=fasta.id)
            i+=1
            session.add(bp)
    
        session.commit()
        # Add a fasta track
        fasta_track = Track(
            track_name = "Fasta Test Track",
            user_id = u_id,
            data_type = "fasta",
            data_id = fasta.id,
            file_name = "testFasta.fasta"
        )

        session.add(fasta_track)
        session.commit()
        session.add(ViewTrack(fasta_track.id,view.id))

        # Create a wig track
        wig = Wig(chrom='EBV1')
        session.add(wig)
        session.commit()

        for pos in range(1,10):
            wig_val = WigValue(
                position = pos,
                value = 1,
                wig_id = wig.id
            )
            session.add(wig_val)   
        
        # add the track
        wig_track = Track(
            track_name = "Wig Test Track",
            user_id = u_id,
            data_type = "wig",
            data_id = wig.id,
            file_name = "testWig.wig"
        )

        session.add(wig_track)
        session.commit()
        session.add(ViewTrack(wig_track.id,view.id))

        # Create a GTF track
        gtf = Gtf()
        session.add(gtf)
        session.commit()

        for pos in range(1,10):
            gtf_val = GtfValue(
                seqname = "EBV1",
                source = "mRNA-Seq",
                feature = "exon",
                start = pos,
                end = pos + 10,
                score = 0,
                strand = "+",
                frame = 0,
                attribute = "spanning-juncs=false;host=hg19",
                gtf_id = gtf.id
            )
            session.add(gtf_val)

        gtf_track = Track(
            track_name = "Gtf Test Track",
            user_id = u_id,
            data_type = "gtf",
            data_id = gtf.id,
            file_name = "testGtf.gtf"
        )

        session.add(gtf_track)
        session.commit()
        session.add(ViewTrack(gtf_track.id,view.id))

        # last make a bed
        bed = Bed()
        session.add(bed)
        session.commit()

        for pos in range(1,10):
            bed_val = BedValue(
                chrom = "EBV1",
                start = pos,
                end = pos+9,
                name = "BED-THING",
                score = 0,
                strand = "+",
                thick_start = pos,
                thick_end = pos+9,
                item_rgb = 10,
                block_count = 1,
                bed_id = bed.id
            )
            session.add(bed_val)
            session.commit()
            
            bb_size = BedBlockSize(
                index = pos,
                value = pos+9,
                bed_value_id = bed_val.id
            )

            bb_start = BedBlockStart(
                index = pos,
                value = pos,
                bed_value_id = bed_val.id
            )
            session.add_all([bb_size, bb_start])
            session.commit()

        bed_track = Track(
            track_name = "Bed Test Track",
            user_id = u_id,
            data_type = "bed",
            data_id = bed.id,
            file_name = "testBED.bed"
        )

        session.add(bed_track)
        session.commit()

        session.add(ViewTrack(bed_track.id,view.id))
        session.commit()

def main():
    parser = argparse.ArgumentParser(description='Manage this Flask application.')
    parser.add_argument('command', help='the name of the command you want to run')
    parser.add_argument('--seedfile', help='the file with data for seeding the database')
    args = parser.parse_args()

    if args.command == 'create_db':
        create_db()
        print "DB created!"

    elif args.command == 'delete_db':
        drop_db()
        print "DB deleted!"

    elif args.command == 'seed_db':
        seed_db()
        print "DB seeded!"

if __name__ == '__main__':
    main()
