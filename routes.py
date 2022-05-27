from flask import Blueprint, render_template, redirect, request, flash, session, g, jsonify, url_for
import requests
from models import Saved_Activity, db, User, User_Activity
from forms import UserAddForm, LoginForm, UpdateUserForm, SavedActivityForm
from sqlalchemy.exc import IntegrityError
from API import BORED_API

bp_routes = Blueprint('/bp_routes', __name__, template_folder='templates')


CURR_USER_KEY = "curr_user"

# region User signup/login/logout

@bp_routes.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@bp_routes.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('user/signup.html', form=form)


@bp_routes.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('user/login.html', form=form)


@bp_routes.route('/logout')
def logout():
    """Handle logout of user."""
    
    do_logout()
    flash("You've been logged out successfully.", "success")
    return redirect('/login')

# endregion

# region Main Routes

@bp_routes.route('/')
@bp_routes.route('/home')
def home_page():
    '''Home page'''
    
    return render_template('home.html')


@bp_routes.route('/activity')
def activity_page():
    """Activity page"""
    
    return render_template("activity.html")

@bp_routes.route('/activity/save', methods=(['POST']))
def handle_saved_activity():
    """Save activity on DB"""
    
    form = SavedActivityForm()
    user=g.user
    
    user_activity = User_Activity(
        title= form.title.data,
        type=form.type.data,
        participants=form.participants.data,
        price=form.price.data,
        key=form.key.data,
        user_id=user.id,
    )
    
    db.session.add(user_activity)
    db.session.commit()
    
    return redirect("/activity")

@bp_routes.route('/activity/ignore', methods=(['POST']))
def handle_ignored_activity():
    """Ignore activity on DB"""
    
    return redirect("activity.html")

# endregion

# region User Routes

@bp_routes.route('/user/<int:user_id>', methods=(['GET']))
def users_show(user_id):
    """Show user profile."""
    
    user = User.query.get_or_404(user_id)
    
    return render_template('profile.html', user=user)

@bp_routes.route('/user/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

# endregion


# region API Routes

@bp_routes.route('/api/activity')
def get_random_activity():
    """Activity page"""
    
    resp = requests.get(BORED_API)
    data = resp.json()
    return data
   

# endregion