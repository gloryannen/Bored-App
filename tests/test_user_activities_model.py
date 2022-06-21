"""User_Activity tests."""

# run these tests like:
#
#    python -m unittest tests/test_user_activities_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import User_Activity, db, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///bored_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test user_activities model."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 4444
        u = User.signup("testing", "testing@testing.com", "password")
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_user_activity_model(self):
        """Does basic model work"""
        
        u_a = User_Activity(
            title="Test application",
            participants="1",
            type="busywork",
            price="0.0",
            isCompleted=True,
            user_id = self.uid
        )
        
        db.session.add(u_a)
        db.session.commit()
        
        self.assertEqual(len(self.u.user_activities), 1)
        self.assertEqual(self.u.user_activities[0].isCompleted, True)

        




        

