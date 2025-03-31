from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,EmailField,IntegerField,SelectField
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

class RandomMovieForm(FlaskForm):
    year = StringField('Year')
    category = SelectField('Category', validators=[DataRequired()],
                            choices=[(0, ""),
                                    (28, "Action"),
                                    (12, "Adventure"),
                                    (16, "Animation"),
                                    (35, "Comedy"),
                                    (80, "Crime"),
                                    (99, "Documentary"),
                                    (18, "Drama"),
                                    (10751, "Family"),
                                    (14, "Fantasy"),
                                    (36, "History"),
                                    (27, "Horror"),
                                    (10402, "Music"),
                                    (9648, "Mystery"),
                                    (10749, "Romance"),
                                    (878, "Science Fiction"),
                                    (10770, "TV Movie"),
                                    (53, "Thriller"),
                                    (10752, "War"),
                                    (37, "Western")])
    submit = SubmitField('Get a movie')

