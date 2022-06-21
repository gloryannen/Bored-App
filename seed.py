'''Seed file to make sample data for users db'''

from models import *
from app import *

# Create all tables
db.drop_all()
db.create_all()

# Add users
testuser = User.signup(username='testuser', email='testuser@test.com', password='test123456789')

saved1 = User_Activity(title="Bake cookies", type="cooking", participants="1", price="0.0", user_id="1")
saved2 = User_Activity(title="Visit a park", type="recreational", participants="1", price="0.0", user_id="1")
saved3 = User_Activity(title="Make clay art", type="diy", participants="1", price="0.1", user_id="1")
completed1 = User_Activity(title="Visit Las Vegas", type="recreational", participants="1", price="0.8", note="Won lots of money with my friend Jordan!", isCompleted=True, user_id="1", timestamp=datetime(2020, 1, 9, 1, 45, 8, 910623))
completed2 = User_Activity(title="Plan picnic day", type="relaxation", participants="1", price="0.0", note="Definitely have to do this next time with the kids!", isCompleted=True, user_id="1", timestamp=datetime(2022, 11, 27, 8, 12, 9, 910623))
ignored1 = Ignored_Activity(title="Make a will", key="123", user_id="1")
ignored2 = Ignored_Activity(title="Jump off a bridge", key="456", user_id="1")
ignored3 = Ignored_Activity(title="Sky diving", key="789", user_id="1")

# Commit to db
db.session.add(testuser)
db.session.commit()

db.session.add_all([saved1, saved1, saved1, completed1, completed2, ignored1, ignored2, ignored3])
db.session.commit()