"""SQLAlchemy models for Bored."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )
   

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

  
    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,   
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Activity(db.Model):
    """Activities in the system."""
    
    __tablename__ = "activities"
    
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    title = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    
    type = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    
    participants = db.Column(
        db.Integer,
        default="1",
    )
    
    price_range = db.Column(
        db.Float,
        default="0.0",
    )
    
class User_Activities(db.Model):
    """User activities."""   
    
    __tablename__ = "user_activities"
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
    )
    
class Tag(db.Model):
    """Tags created by users."""   
    
    __tablename__ = "tags"
    
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    title = db.Column(
        db.Text,
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        primary_key=True,
    )
    
class Activities_Tag(db.Model):
    """Tags in Activities."""
    
    __tablename__ = "activities_tag"
    
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id", ondelete="cascade"),
        primary_key=True,
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        primary_key=True,
    )
    
class Note(db.Model):
    """Notes created by user."""
    
    __tablename__ = "notes"
    
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    text = db.Column(
        db.Text,
    )
    
    activity_id = db.Column(
        db.Integer,
        db.ForeignKey("activities.id"),
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
    )
    
    
    
def connect_db(app):
    """Connect db to app"""
    db.app = app
    db.init_app(app)
