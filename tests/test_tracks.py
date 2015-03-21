from flask.ext.testing import TestCase
import unittest
import angular_flask
from flask import Flask, json, jsonify
from angular_flask import app, db, session
from angular_flask.models import User,Track

import logging
logging.basicConfig()
LOG = logging.getLogger(__name__)

class TrackTestCase(TestCase):
    STATUS_OK = "200 OK"

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
        response = self.app.post('/tracks', 
            data=json.dumps({
                'track_name': 'kyles track', 
                'data_type': 'wig',
                'data_id':'1',
                'file_name':'mywig.wig'
            }), 
            content_type='application/json',
            headers={"X-UserId":"1"})

        self.assert200(response)
        self.assertEqual(json.loads(response.get_data()).get('track_id'),1)

    def testGetTrack(self):
        LOG.info("Testing track endpoint /tracks/<track_id> with GET")#

        # Helper to create a user + track (has already been tested above)
        self.createTestUser()
        self.createTestTrack()

        # Check the user json returned
        response = self.app.get('/tracks/1',headers={"X-UserId":"1"})
        self.assert200(response)

        # Make sure the user dict has the right fields
        track = json.loads(response.get_data())
        print track
        self.assertDictContainsSubset({
                'track_id' : '1',
                'track_name':'kyles track',
                'data_type':'wig',
                'data_id':'1',
                'user_id':'1',
                'file_name':'mywig.wig'
            },
            track
        )

#    def test_get_nonexistant_user(self):
#        """
#        Try to GET a user by an invalid id
#        """
#        response = self.app.get('/users/1')
#        self.assert404(response)
#
#    def testPutUser(self):
#        LOG.info("Testing user endoint /users/<user_id> with PUT")
#        self.createTestUser()
#        user = self.getTestUser()
#        user['user_name'] = "KYLES NEW NAME"
#
#        # Handle put request
#        updated_json = json.dumps(user)
#        response = self.app.put('/users/'+str(user.get('user_id')), 
#            data=updated_json, 
#            content_type='application/json')
#        self.assert200(response)
#        
#        # Check that PUT response matches request data
#        json_up = json.loads(response.get_data())
#        self.assertEqual(user,json_up)
#
#        # Check that changes are still there when we GET
#        user_refresh = self.getTestUser()
#        self.assertEqual(user_refresh,json_up)
#
#    def testDeleteUser(self):
#        LOG.info("Testing user endpoint /users/<user_id> with DELETE")
#        self.createTestUser()
#        user = self.getTestUser()
#        user_id = str(user.get('user_id'))
#        response = self.app.delete('/users/'+user_id)
#        self.assert200(response)
#
#        # Check if we can still GET
#        response_get = self.app.get('/users/{uid}'.format(uid=user_id))
#        self.assert404(response_get)
#
    def createTestUser(self):
        response = self.app.post('/users', 
            data=json.dumps({'user_name': 'kyle', 'email': 'kyle@email.com'}), 
            content_type='application/json')
    
    def createTestTrack(self):
        response = self.app.post('/tracks', 
            data=json.dumps({
                'track_name': 'kyles track', 
                'data_type': 'wig',
                'data_id':'1',
                'file_name':'mywig.wig'
            }), 
            content_type='application/json',
            headers={"X-UserId":"1"})


if __name__ == '__main__':
    unittest.main()

