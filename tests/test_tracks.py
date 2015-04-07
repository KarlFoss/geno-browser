from flask.ext.testing import TestCase
import unittest
import gb
from flask import Flask, json, jsonify
from gb import app, db, session
from gb.models import User,Track

import logging
logging.basicConfig()
LOG = logging.getLogger(__name__)

class TrackTestCase(TestCase):
    user_header = {"X-Userid":1}

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

    def testCreateTrack(self):
        LOG.info("Testing create track endpoint /tracks with POST")

        # first create a user
        self.createTestUser()

        # Send post request
        response = self.app.post('/api/tracks', 
            data=json.dumps({
                'track_name': 'kyles track', 
                'data_type': 'wig',
                'data_id':1,
                'file_name':'mywig.wig'
            }), 
            content_type='application/json',
            headers=self.user_header)

        self.assert200(response)
        self.assertEqual(json.loads(response.get_data()).get('track_id'),1)

    def testGetTrack(self):
        LOG.info("Testing track endpoint /tracks/<track_id> with GET")

        # Helper to create a user + track (has already been tested above)
        self.createTestUser()
        self.createTestTrack()

        # Check the user json returned
        response = self.app.get('/api/tracks/1',headers=self.user_header)
        self.assert200(response)

        # Make sure the user dict has the right fields
        track = json.loads(response.get_data())
        self.assertDictContainsSubset({
                'track_id' : 1,
                'track_name':'kyles track',
                'data_type':'wig',
                'data_id':1,
                'user_id':1,
                'file_name':'mywig.wig'
            },
            track
        )

    def testGetNonexistantTrack(self):
        response = self.app.get('/api/tracks/1',headers=self.user_header)
        self.assert404(response)

    def testPutTrack(self):
        LOG.info("Testing track endoint /api/tracks/<track_id> with PUT")
        self.createTestUser()
        self.createTestTrack()
        track = self.getTestTrack()
        track['track_name'] = "New_TRACK_NAME"

        # Handle put request
        updated_json = json.dumps(track)
        response = self.app.put('/api/tracks/'+str(track.get('track_id')), 
           data=updated_json, 
           content_type='application/json',
           headers=self.user_header
        )
        self.assert200(response)

        # Check that PUT response matches request data
        json_up = json.loads(response.get_data())
        self.assertEqual(track,json_up)

        # Check that changes are still there when we GET
        track_refresh = self.getTestTrack()
        self.assertEqual(track_refresh,json_up)

    def testDeleteTrack(self):
        LOG.info("Testing track endpoint /api/track/<track_id> with DELETE")
        self.createTestUser()
        self.createTestTrack()
        track = self.getTestTrack()
        track_id = str(track.get('track_id'))
        response = self.app.delete('/api/tracks/{}'.format(track_id),
            headers=self.user_header
        )
        self.assert200(response)

        # Check if we can still GET
        response_get = self.app.get('/api/tracks/{}'.format(track_id))
        self.assert404(response_get)

    def createTestUser(self):
        response = self.app.post('/api/users', 
            data=json.dumps({'username': 'kyle', 'email': 'kyle@email.com'}), 
            content_type='application/json')
    
    def createTestTrack(self):
        response = self.app.post('/api/tracks', 
            data=json.dumps({
                'track_name': 'kyles track', 
                'data_type': 'wig',
                'data_id':1,
                'file_name':'mywig.wig'
            }), 
            content_type='application/json',
            headers=self.user_header)

    def getTestTrack(self):
        response = self.app.get('/api/tracks/1',
            headers=self.user_header
        )
        track = json.loads(response.get_data())
        return track


if __name__ == '__main__':
    unittest.main()

