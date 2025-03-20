from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,EmailField
from wtforms.validators import DataRequired, EqualTo, Email


class RegisterForm(FlaskForm):
    name = StringField("User Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Check your password",
                              validators=[DataRequired()])

    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


