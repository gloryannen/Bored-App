from flask import (
    Blueprint,
    render_template,
    redirect,
    flash,
    session,
    g,
    
)
import json
import requests
from datetime import datetime
from activity_helper import *
from models import db, User, User_Activity, Ignored_Activity
from forms import IsCompleted, UserAddForm, LoginForm, UpdateUserForm, SavedActivityForm, ActivitySearchCriteria, IgnoreActivityForm, NoteForm
from sqlalchemy.exc import IntegrityError
from API import BORED_API

bp_routes = Blueprint("/bp_routes", __name__, template_folder="templates")

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


@bp_routes.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle user signup. Create new user and add to DB. Redirect to home page. 
    If form not valid, present form. 
    If the there already is a user with that username: flash message and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("user/signup.html", form=form)
        
        do_login(user)

        return redirect("/")

    else:
        return render_template("user/signup.html", form=form)


@bp_routes.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcome, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')
        
    return render_template("user/login.html", form=form)


@bp_routes.route("/logout")
def logout():
    """Handle logout of user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        flash(f"You have successfully logged out!", "success")
    return redirect("/login")

# endregion

# region Main Routes

@bp_routes.route("/")
def homepage():
    """Show homepage and load random activity"""
    
    resp = requests.get(BORED_API)
    data = resp.json()
    
    return render_template('home.html', data=data)
        
@bp_routes.route("/user/<int:user_id>")
def index(user_id):
    """Show user profile with activity summary"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    if g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(user_id)
    
    completed = (User_Activity.query.filter(User_Activity.user_id == user_id, User_Activity.isCompleted == True).all())
    
    return render_template("user/profile.html", user=user, completed=completed)


@bp_routes.route("/user/<int:user_id>/saved_activity")
def saved_activity_page(user_id):
    """Saved activity page"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    if g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(user_id)
    
    activities = (User_Activity.query.filter(User_Activity.user_id == user_id).order_by(User_Activity.isCompleted == False, User_Activity.timestamp.asc()).all())
    
    return render_template("activities/activity.html", user=user, activities=activities)

@bp_routes.route("/user/<int:user_id>/completed_activities", methods=["GET", "POST"])
def completed_activity_page(user_id):
    """Completed activity page"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    if g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form=NoteForm()
  
    completed = (User_Activity.query.filter(User_Activity.user_id == user_id, User_Activity.isCompleted == True).all())
    
    return render_template("activities/completed_activities.html", completed=completed, form=form)

@bp_routes.route("/activity_completed/<int:user_activities_id>/remove", methods=["Post"])
def remove_completed_activity(user_activities_id):
    """Remove activity from completed list."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    activity = User_Activity.query.get_or_404(user_activities_id)
    
    db.session.delete(activity)
    db.session.commit()
    flash("Activity has been removed.", "success")

    return redirect(f"/user/{g.user.id}/completed_activities")

@bp_routes.route("/user/<int:user_id>/ignored_activities")
def ignored_activity_page(user_id):
    """Ignored activity page"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    if g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(user_id)
    
    activities = (Ignored_Activity.query.filter(Ignored_Activity.user_id == user_id).limit(30).all())
    
    return render_template("activities/ignored_activities.html", user=user, activities=activities)

@bp_routes.route("/activity/<int:ignored_activities_id>/remove", methods=["Post"])
def remove_activity(ignored_activities_id):
    """Remove activity from ignored list."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    activity = Ignored_Activity.query.get_or_404(ignored_activities_id)
    
    db.session.delete(activity)
    db.session.commit()
    flash("Activity has been removed.", "success")

    return redirect(f"/user/{g.user.id}/ignored_activities")

@bp_routes.route("/activity/save", methods=(["POST"]))
def handle_saved_activity():
    """Save activity on DB"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = g.user
    form = SavedActivityForm()

    user_activity = User_Activity(
        title=form.title.data,
        type=form.type.data,
        participants=form.participants.data,
        price=form.price.data,
        key=form.key.data,
        user_id=user.id,
    )
    db.session.add(user_activity)
    db.session.commit()
    flash("Activity has been saved.", "success")
 
    return redirect(f"/user/{user.id}/new_activity")


@bp_routes.route("/activity/ignore", methods=(["POST"]))
def handle_ignored_activity():
    """Ignore activity on DB"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = IgnoreActivityForm()
    user = g.user
    
    ignored_activity = Ignored_Activity(
        title=form.title.data,
        key=form.key.data,
        user_id=user.id,
    )

    db.session.add(ignored_activity)
    db.session.commit()
    flash("Activity has been ignored.", "success")

    return redirect(f"/user/{user.id}/new_activity")


# endregion

# region User Routes

@bp_routes.route("/user/<int:user_id>/new_activity", methods=(["GET"]))
def new_activity(user_id):
    """New activity page."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    if g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
 
    form = ActivitySearchCriteria()
    
    return render_template("activities/new_activity.html", form=form)

@bp_routes.route('/user/<int:user_id>/profile_update', methods=["GET", "POST"])
def profile_update(user_id):
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    if g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    
    form = UpdateUserForm(obj=user)
    
    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
        
            db.session.commit()
            return redirect(f"/user/{user.id}")
        flash("Password incorrect, try again", "danger")
    
    return render_template('/user/edit.html', user_id=user.id, form=form)


@bp_routes.route("/user/delete", methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    session.pop("username", None)

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


# endregion

# region Note Routes
@bp_routes.route("/note/add", methods=(["GET","POST"]))
def add_note():
    """Add note to activity"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = g.user
    form = NoteForm()
    
    id = form.id.data
    note = form.note.data
    
    activity=User_Activity.query.get(id)
    activity.note = note
    
    db.session.commit()
    
    return redirect(f"/user/{user.id}/completed_activities")

# endregion

# region API Routes

@bp_routes.route("/api/activity")
def get_random_activity():
    """Activity page"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = g.user
    resp = requests.get(BORED_API)
    data = resp.json()
    ignored = Ignored_Activity.query.filter(Ignored_Activity.user_id == user.id).all()
    isIgnored = False
    for x in ignored:
            if int(x.key) == int(data['key']):
                isIgnored = True
    
    if isIgnored:
        maxRetry= 3
        for x in range(maxRetry):
            newResp = requests.get(BORED_API)
            newData = newResp.json()
            setIgnored = False
            for x in ignored:
                if int(x.key) == int(data['key']):
                    setIgnored = True
            
            if not setIgnored:
                return newData
            
        return "Tried but no data found"
    return data    

@bp_routes.route("/api/activity2", methods=["GET","POST"])
def get_searched_activity():
    """Activity page"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = g.user
    form=ActivitySearchCriteria()
    
    typeValues=form.activityType.data[0].split(",")
    randomVariables = assignRandVariable(form.price.data, form.participants.data, typeValues)

    resp = requests.get(f"{BORED_API}?minprice=0&maxprice={randomVariables.price}&participants={randomVariables.participants}&type={randomVariables.type}")
    data = resp.json()
    ignored = Ignored_Activity.query.filter(Ignored_Activity.user_id == user.id).all()
    isIgnored = False
    if "key" in data:
        for x in ignored:
            if int(x.key) == int(data['key']):
                isIgnored = True
        
    if "error" in data or isIgnored:
        maxRetry = 20
        for x in range(maxRetry):
            tryRandomVariables = assignRandVariable(form.price.data, form.participants.data, typeValues)
            
            testresp = requests.get(f"{BORED_API}?minprice=0&maxprice={tryRandomVariables.price}&participants={tryRandomVariables.participants}&type={tryRandomVariables.type}")
            testdata= testresp.json()
            testignored = False
            if "key" in testdata:
                for x in ignored:
                    if int(x.key) == int(testdata['key']):
                        testignored = True
            
            if "error" not in testdata or testignored:
                return testdata
        
        return "Tried but no data found"
        
    return data

@bp_routes.route("/api/set_completed", methods=["GET","POST"])
def set_completed_activity():
    """Handle completed/uncompleted activity"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form=IsCompleted()
    
    id = form.id.data
    isCompleted = form.isCompleted.data
    
    activity=User_Activity.query.get(id)
    activity.isCompleted = isCompleted
    activity.timestamp = datetime.utcnow()
    
    db.session.commit()

# endregion
