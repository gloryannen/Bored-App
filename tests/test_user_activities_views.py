"""User View tests."""

# run these tests like:
#
#    python -m unittest tests/test_user_activities_views.py

import json
import os
import requests
from unittest import TestCase
from bs4 import BeautifulSoup
from models import Ignored_Activity, db, connect_db, User, User_Activity

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///bored_test"


# Now we can import app

from app import app
from routes import CURR_USER_KEY
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()
        self.client = app.test_client()

        self.testuser = User.signup("tester", "tester@test.com", "password")
        self.testuser_id = 1
        
        self.testuser2 = User.signup("tester2", "tester2@test.com", "password")
        self.testuser2_id = 2
        
        db.session.commit()
        
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def setup_activities(self):
        saved1 = User_Activity(title="test", type="busywork", participants="1", price="0.0",user_id=self.testuser_id)
        saved2 = User_Activity(title="test2", type="busywork", participants="1", price="0.0", user_id=self.testuser_id)
        completed1 = User_Activity(title="Completed test", type="busywork", participants="1", price="0.0", isCompleted=True, user_id=self.testuser_id)
        ignored = Ignored_Activity(title="Ignored test", key="4444", user_id=self.testuser_id)
        db.session.add_all([saved1, saved2, completed1, ignored])
        db.session.commit()
   
    def test_user_activities_show(self):
        self.setup_activities()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                
            # Check saved activity page has 2 activities    
            resp = c.get(f"/user/{self.testuser_id}/saved_activity")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("test", str(resp.data))
            self.assertIn("test2", str(resp.data))
            
            # Check completed activities has 1 completed activity
            resp = c.get(f"/user/{self.testuser_id}/completed_activities")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Completed test", str(resp.data))
            self.assertNotIn("test2", str(resp.data))
            
            # Check completed activities has 1 ignored activity
            resp = c.get(f"/user/{self.testuser_id}/ignored_activities")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Ignored test", str(resp.data))
            self.assertNotIn("test2", str(resp.data))
    
    def test_complete_activity(self):
        self.setup_activities()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                
            resp = c.post("/api/set_completed", data={"activity_Id": "1", "isCompleted": "checked"})
            
            self.assertEqual(resp.status_code, 200)
            resp = c.get(f"/user/{self.testuser_id}/completed_activities")
            
            # Check that the new activity that has been checked shows in completed activities page
            self.assertIn("test", str(resp.data))
            self.assertIn("Completed test", str(resp.data))
            
    def test_user_remove_completed_activity(self):
        self.setup_activities()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            resp = c.post("/activity_completed/3/remove", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
        
            # Check that the activity has been removed from completed_activities
            response = c.get(f"/user/{self.testuser_id}/completed_activities")
            self.assertNotIn("Completed test", str(response.data))
    
    def test_user_remove_ignored_activity(self):
        self.setup_activities()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                
            resp = c.post(f"/activity/1/remove", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            
            # Check that the activity has been removed from ignored_activities
            resp = c.get(f"/user/{self.testuser_id}/ignored_activities")
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Ignored test", str(resp.data))

                 
            
          
                
       
                