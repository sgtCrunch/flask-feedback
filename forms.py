from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, ValidationError, PasswordField
from wtforms.validators import InputRequired, Optional, Email, length

class AddUserForm(FlaskForm):
    """Form for adding Users"""

    username = StringField("Username",
                            validators=[InputRequired(), length(min=8,max=20)])
    password = PasswordField("Password",
                            validators=[InputRequired(), length(min=8)])
    email = StringField("Email",
                            validators=[InputRequired(), Email()])
    first_name = StringField("First Name",
                            validators=[InputRequired()])
    last_name = StringField("Last Name",
                            validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for loging in Users"""

    username = StringField("Username",
                            validators=[InputRequired(), length(min=8,max=20)])
    password = PasswordField("Password",
                            validators=[InputRequired(), length(min=8)])
    

class AddFeedback(FlaskForm):
    """Form for loging in Users"""

    title = StringField("Title",
                            validators=[InputRequired(), length(max=100)])
    content = TextAreaField("Content",
                            validators=[InputRequired()])