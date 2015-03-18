from flask.ext.testing import TestCase
import unittest
import angular_flask
from flask import Flask, json, jsonify
from angular_flask import app, db, session
from angular_flask.models import User

class UserTestCase(TestCase):
    STATUS_OK = "200 OK"

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        print "#" * 40
    	app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/angular_flask.db'

        # we set self to the app instance
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
    	db.session.remove()
        db.drop_all()

    def testCreateUser(self):
        print "Testing create user endpoint /users with POST"

        # Send post request
        response = self.app.post('/users', 
            data=json.dumps({'user_name': 'kyle', 'email': 'kyle@email.com'}), 
            content_type='application/json')

        assert response.status == self.STATUS_OK 
        assert json.loads(response.get_data()).get('user_id') == 1

    def testGetUser(self):
        print "Testing user endpoint /users/<user_id> with GET"

        # Helper to create a user (has already been tested above)
        self.createTestUser()

        # Check the user json returned
        response = self.app.get('/users/1')
        assert response.status == self.STATUS_OK

        # Make sure the user dict has the right fields
        user = json.loads(response.get_data())
        assert user.get('user_name') == 'kyle'
        assert user.get('email') == 'kyle@email.com'

    def testPutUser(self):
        print "Testing user endoint /users/<user_id> with PUT"
        self.createTestUser()
        user = self.getTestUser()
        user['user_name'] = "KYLES NEW NAME"

        # Handle put request
        updated_json = json.dumps(user)
        response = self.app.put('/users/'+str(user.get('user_id')), 
            data=updated_json, 
            content_type='application/json')
        assert response.status == self.STATUS_OK
        

        json_up = json.loads(response.get_data())
        assert json_up.get('user_id') == user.get('user_id')
        assert json_up.get('email') == user.get('email')
        assert json_up.get('user_id') == user.get('user_id')

    def testDeleteUser(self):
        print "Testing user endpoint /users/<user_id> with DELETE"
        self.createTestUser()
        user = self.getTestUser()
        user_id = str(user.get('user_id'))
        response = self.app.delete('/users/'+user_id)

    def createTestUser(self):
        response = self.app.post('/users', 
            data=json.dumps({'user_name': 'kyle', 'email': 'kyle@email.com'}), 
            content_type='application/json')

    def getTestUser(self):
        response = self.app.get('/users/1')
        user = json.loads(response.get_data())
        return user


if __name__ == '__main__':
    unittest.main()