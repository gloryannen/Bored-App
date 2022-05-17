"""Bored Application"""

import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
from routes import bp_routes

app = Flask(__name__)
app.register_blueprint(bp_routes)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///bored_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()