from flask import Blueprint, render_template, redirect, request
from models import db

bp_routes = Blueprint('/bp_routes', __name__, template_folder='templates')

CURR_USER_KEY = "curr_user"

# region Main Routes

@bp_routes.route('/')
@bp_routes.route('/home')
def home_page():
    '''Home page'''
    
    return render_template('home.html')
# endregion

# region User Routes
# endregion