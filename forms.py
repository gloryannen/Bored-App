from flask_wtf import FlaskForm
from sqlalchemy import Float, Integer
from wtforms import StringField, PasswordField, HiddenField, FloatField, IntegerField, SelectMultipleField, IntegerRangeField, DecimalRangeField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange

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
        
class IgnoreActivityForm(FlaskForm):
    """Save activity form."""
    
    title = HiddenField(name="activityTitle")
    key = HiddenField(name="activityKey")
    
class ActivitySearchCriteria(FlaskForm):
    """Activity Criteria form."""
    
    participants = IntegerRangeField("Participants (1 to 3+)", id="formParticipants",validators=[NumberRange(min=1, max=3)], default=1)
    price = DecimalRangeField("Price Range (from free to $$$)", id="formPrice",validators=[NumberRange(min=0, max=1)], places=.01, default=1)
    activityType = SelectMultipleField("Activity Type", id="formActivityType",choices=[("busywork", "Busywork"), ("charity", "Charity"), ("cooking", "Cooking"), ("diy", "DIY"), ("education", "Education"), ("music", "Music"), ("recreational", "Recreational"), ("relaxation", "Relaxation"), ("social", "Social")], default=["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"])
    
class IsCompleted(FlaskForm):
    """Handle completed activity"""
    id= IntegerField(name="activity_Id")
    isCompleted=BooleanField(name="isCompleted")