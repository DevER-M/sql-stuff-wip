from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(),Length(3,30)])
    email = EmailField("email",validators=[Email(),DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = EmailField("email",validators=[Email(),DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    submit = SubmitField("Log In")