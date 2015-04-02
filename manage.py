import os
import json
import argparse
import requests
import random

from gb import app,db,session
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

    # add the users
    user_ids = []
    users = ["default","kyle","karl","coda","max","goof"]
    for name in users:
        new_user = User(username=name,email="{}@email.com".format(name))
        session.add(new_user)
        session.commit()
        user_ids.append(new_user.id)

    ## Give each a track ##
    for u_id in user_ids:

        view = View(view_name = "Test View")
        session.add(view)
        session.commit()

        # Create a fasta and a wig data set, tracks, and a view holding them
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
            data_id = 1,
            file_name = "testFasta.fasta",
        )

        session.add(fasta_track)
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

if __name__ == '__main__':
    main()
