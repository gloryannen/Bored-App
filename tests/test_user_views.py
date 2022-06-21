"""User View tests."""

# run these tests like:
#
#    python -m unittest tests/test_user_views.py

import json
import os
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
   
    def test_user_profile(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
             
            resp = c.get(f"/user/{self.testuser_id}", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

    def setup_activities(self):
        saved1 = User_Activity(title="test", type="busywork", participants="1", price="0.0",user_id=self.testuser_id)
        saved2 = User_Activity(title="test2", type="busywork", participants="1", price="0.0", user_id=self.testuser_id)
        completed1 = User_Activity(title="Completed test", type="busywork", participants="1", price="0.0", isCompleted=True, user_id=self.testuser_id)
        ignored = Ignored_Activity(title="Ignored test", key="4444", user_id=self.testuser_id)
        db.session.add_all([saved1, saved2, completed1, ignored])
        db.session.commit()
   
    def test_user_profile_activity_summary(self):
        self.setup_activities()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                
            resp = c.get(f"/user/{self.testuser_id}")
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("TESTER", str(resp.data))
            
            soup = BeautifulSoup(str(resp.data), 'html.parser')
            found = soup.findAll('li', {"class": "list-group-item"})
            print(found)
            self.assertEqual(len(found), 3)

            # Test for a count of 3 saved activities 
            self.assertIn("3", found[0].text)

            # Test for a count of 1 completed activity
            self.assertIn("1", found[1].text)

            # Test for a count of 1 ignored activity
            self.assertIn("1", found[2].text)

    
    def test_user_edit_profile(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                
            resp = c.get(f"/user/{self.testuser_id}/profile_update")
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("To confirm changes, enter your password:", str(resp.data))
            
    def test_user_can_update_profile(self):
         with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                
            resp = c.post(f"/user/{self.testuser_id}/profile_update", json={"username": "updatedTester", "password": "password"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            
            # Check that the username has been updated in profile
            response = c.get(f"/user/{self.testuser_id}/profile_update")
            self.assertIn("updatedTester", str(response.data))
    
    def test_user_can_be_removed(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                
            resp = c.post(f"/user/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            
            # Unauthenticated users received Sign Up button in Homepage
            response = c.get(f"/", follow_redirects=True)
            self.assertIn("Sign up", str(response.data))
                 
            
          
                
       
                