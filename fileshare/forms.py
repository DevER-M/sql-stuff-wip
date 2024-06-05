from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from fileshare.models import User


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(3, 30)])
    email = EmailField("email", validators=[Email(), DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), Length(3)])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already in use :(")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already in use :(, Login?")


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[Email(), DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class AddFileForm(FlaskForm):
    file = FileField("Upload File", validators=[DataRequired()])
    submit = SubmitField("Upload")
