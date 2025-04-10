from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from . import db
from .models import User, RandomMovie
from .forms import RegisterForm, LoginForm
from .email_sender import Email, generate_unique_code

auth = Blueprint("auth", __name__)

@auth.route('/register', methods= ["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        passw = form.password1.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if user:
            flash("User already exists." ,'error')
            return redirect(url_for('auth.register'))
        elif form.password1.data != form.password2.data:
            flash("Passwords must be the same." ,'error')
            return redirect(url_for('auth.register'))
        elif len(form.password1.data) < 8:
            flash("Password must have minimum 8 characters." ,'error')
            return redirect(url_for('auth.register'))
        elif not special_char(form.password1.data):
            flash("Password must have one special character." ,'error')
            return redirect(url_for('auth.register'))
        #hasing and salting a password
        password = generate_password_hash(password= passw,
                                          method= "pbkdf2:sha256",
                                          salt_length= 8)

        new_user = User(email= email,
                        password= password,
                        name= name,
                        confirmation_code= generate_unique_code(),
                        confirmation = False)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        first_movie = RandomMovie(unique_id= 000000,
                                title= "Let us give you a movie",
                                overview= "We are glad to help you watch a movie today.",
                                poster_url= "",
                                rating = 10,
                                trailer= "",
                                release_date="0000",
                                movie_owner= current_user.id)
        db.session.add(first_movie)
        db.session.commit()

        mail = Email(name, email, new_user.id, new_user.confirmation_code)
        mail.create_email()
        mail.send_email(email)
        flash('Cont creat cu succes. Verifica emailul, pentru confirmare.')

        return redirect(url_for('views.home', logged_in= current_user.is_authenticated))
    return render_template("register.html",form= form ,logged_in= current_user.is_authenticated)

@auth.route('/login', methods= ["GET", "POST"])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password1.data

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            error = "User does not exist."
        elif not check_password_hash(user.password, password= password):
            error = "Incorrect password."
        else:
            flash("You were succesfully logged in")
            login_user(user)
            return redirect(url_for('views.show_profile', user_id= current_user.id))


    return render_template("login.html",form= form, error= error, logged_in= current_user.is_authenticated)

@auth.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')

@auth.route('/confirm', methods= ['GET'])
def confirmation_account():
    code = request.args.get('code')
    user_id = request.args.get('id')
    print(code)
    user = db.session.execute(db.select(User).where(User.id == int(user_id))).scalar()
    if user:
        if user.confirmation_code == code:
            user.confirmation = True
            db.session.commit()
            flash("Cont confirmat cu succes.")

    return redirect(url_for('views.home'))

def special_char(password):
    special_chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '[', ']', '^', '_', ':', ';', '<', '=', '>', '?', '{', '|', '}']
    for letter in password:
        if letter in special_chars:
            return True
    return False