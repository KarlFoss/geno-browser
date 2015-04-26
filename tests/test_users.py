from flask.ext.testing import TestCase
import unittest
import gb
from flask import Flask, json, jsonify
from gb import app, db, session
from gb.models import User

import logging
logging.basicConfig()
LOG = logging.getLogger(__name__)

class UserTestCase(TestCase):

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

        # setup token
        self.token = ''

    def tearDown(self):
    	db.session.remove()
        db.drop_all()

    def testCreateUser(self):
        LOG.info("Testing create user endpoint /api/users with POST")

        # Send post request
        response = self.app.post('/api/users', 
            data=json.dumps({'username': 'kyle', 'email': 'kyle@email.com','password':'SECRET'}), 
            content_type='application/json')

        self.assert200(response)
        self.assertEqual(json.loads(response.get_data()).get('user_id'), 1)

    def testGetUser(self):
        LOG.info("Testing user endpoint /api/users/ with GET")

        # Helper to create a user (has already been tested above)
        self.createTestUser()

        # Check the user json returned
        response = self.app.get('/api/users/', headers=[('Authorization','Bearer ' + self.token)])
        self.assert200(response)

        # Make sure the user dict has the right fields
        user = json.loads(response.get_data())
        self.assertDictContainsSubset({'username':'kyle','email':'kyle@email.com'},user)

    def test_get_user_no_auth(self):
        """
        Try to GET a user by an invalid id
        """
        response = self.app.get('/api/users/')
        self.assert401(response)

    def testPutUser(self):
        LOG.info("Testing user endoint /api/users/ with PUT")
        self.createTestUser()
        user = self.get_user()

        #Don't change the name because then I need to base64 encode <user:pass> again
        user['email'] = "kyle@hotmail.com"

        # Handle put request
        updated_json = json.dumps(user)
        response = self.app.put('/api/users/', 
            headers=[('Authorization','Bearer ' + self.token)],
            data=updated_json, 
            content_type='application/json')
        self.assert200(response)
        
        # Check that PUT response matches request data
        json_up = json.loads(response.get_data())
        self.assertEqual(user,json_up)

        # Check that changes are still there when we GET
        user_refresh = self.get_user()
        self.assertEqual(user_refresh,json_up)

    def testDeleteUser(self):
        LOG.info("Testing user endpoint /api/users/ with DELETE")
        self.createTestUser()
        user = self.get_user()
        user_id = str(user.get('user_id'))
        response = self.app.delete('/api/users', headers=[('Authorization','Bearer ' + self.token)])
        self.assert200(response)

        # Check if we can still GET
        response_get = self.app.get('/api/users', headers=[('Authorization','Bearer ' + self.token)])
        self.assert400(response_get)

    def createTestUser(self):
        response = self.app.post('/api/users', 
            data=json.dumps({'username': 'kyle', 'email': 'kyle@email.com', 'password':'SECRET'}), 
            content_type='application/json')

        response = self.app.post('api/auth',
            data=json.dumps({'username':'kyle', 'password':'SECRET'}),
            content_type='application/json')

        JSON = json.loads(response.get_data())
        self.token = str(JSON.get('token'))

    def get_user(self):
        response = self.app.get('/api/users', headers=[('Authorization','Bearer ' + self.token)])
        self.assert200(response)
        user = json.loads(response.get_data())
        return user


if __name__ == '__main__':
    unittest.main()
