from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    flash,
    session,
    g,
    url_for,
)
import requests
from models import db, User, User_Activity, Saved_Activity
from forms import UserAddForm, LoginForm, UpdateUserForm, SavedActivityForm
from sqlalchemy.exc import IntegrityError
from API import BORED_API

bp_routes = Blueprint("/bp_routes", __name__, template_folder="templates")

# region User signup/login/logout

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
            session["username"] = form.username.data

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("user/signup.html", form=form)

        return redirect("/")

    else:
        return render_template("user/signup.html", form=form)


@bp_routes.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            session["username"] = request.form["username"]

            user = User.authenticate(form.username.data, form.password.data)

            return redirect("/")

        flash("Invalid credentials.", "danger")
        return render_template("user/login.html", form=form)

    return render_template("user/login.html", form=form)


@bp_routes.route("/logout")
def logout():
    """Handle logout of user."""

    session.pop("username", None)
    flash("You've been logged out successfully.", "success")
    return redirect("/login")


# endregion

# region Main Routes


@bp_routes.route("/")
def index():
    if "username" in session:
        username = session["username"]
        return redirect(f"/user/{username}")
    #   return f"This is {username}"

    return redirect("/login")


@bp_routes.route("/activity")
def activity_page():
    """Activity page"""

    return render_template("activity.html")


@bp_routes.route("/activity/save", methods=(["POST"]))
def handle_saved_activity():
    """Save activity on DB"""

    form = SavedActivityForm()
    user = g.user

    user_activity = User_Activity(
        title=form.title.data,
        type=form.type.data,
        participants=form.participants.data,
        price=form.price.data,
        key=form.key.data,
        user_username=user.username,
    )

    db.session.add(user_activity)
    db.session.commit()

    return redirect("/activity")


@bp_routes.route("/activity/ignore", methods=(["POST"]))
def handle_ignored_activity():
    """Ignore activity on DB"""

    return redirect("activity.html")


# endregion

# region User Routes


@bp_routes.route("/user/<string:username>", methods=(["GET"]))
def users_show(username):
    """Show user profile."""

    user = User.query.get_or_404(username)

    return f"{user} - You are in your own page WOW"


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


# region API Routes


@bp_routes.route("/api/activity")
def get_random_activity():
    """Activity page"""

    resp = requests.get(BORED_API)
    data = resp.json()
    return data


# endregion
