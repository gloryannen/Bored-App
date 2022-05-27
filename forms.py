from flask_wtf import FlaskForm
from sqlalchemy import Float
from wtforms import StringField, PasswordField, HiddenField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)]) 
    
class UpdateUserForm(FlaskForm):
    """Update user details form."""
    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class SavedActivityForm(FlaskForm):
    """Save activity form."""
    
    key = HiddenField(name="activityKey")
    type = HiddenField(name="activityType")
    title = HiddenField(name="activityTitle")
    participants = HiddenField(name="activityParticipants")
    price = HiddenField(name="activityPrice")
        
    