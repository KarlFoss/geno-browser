from flask.ext.testing import TestCase
import unittest
import gb
import io, os
from flask import Flask, json, jsonify
from gb import app, db, session
from gb.models import *

import logging
logging.basicConfig()
LOG = logging.getLogger(__name__)

class TrackTestCase(TestCase):
    user_header = [('Authorization','Basic a3lsZTpTRUNSRVQ=')]

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
    	app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        # Use in-memory database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

        # we set self to the app instance
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
    	db.session.remove()
        db.drop_all()

    def testUploadFasta(self):
        LOG.info("Testing upload of fasta file to endpoint /files with POST")
        test_dir = os.path.dirname(os.path.abspath(__file__))

        # first create a user
        self.createTestUser()

        response = self.app.post('/api/files',
            data=dict(
                file=(open(test_dir+"/../var/B958-short.fasta", 'rb'), 'test.fasta'),
                type="fasta"
            ), 
            follow_redirects=True,
            headers=self.user_header
        )

        self.assert200(response)
        self.assertEqual(json.loads(response.get_data()).get('track_id'),1)

    def testUploadWig(self):
        LOG.info("Testing upload of wig file to endpoint /files with POST")
        test_dir = os.path.dirname(os.path.abspath(__file__))

        # first create a user
        self.createTestUser()

        response = self.app.post('/api/files',
            data=dict(
                file=(open(test_dir+"/../var/shortWig.wig", 'rb'), 'test.wig'),
                type="wig"
            ), 
            follow_redirects=True,
            headers=self.user_header
        )

        self.assert200(response)
        self.assertEqual(json.loads(response.get_data()).get('track_ids'),[1,2,3,4])


    def createTestUser(self):
        response = self.app.post('/api/users', 
            data=json.dumps({'username': 'kyle', 'email': 'kyle@email.com','password':'SECRET'}), 
            content_type='application/json')

if __name__ == '__main__':
    unittest.main()

