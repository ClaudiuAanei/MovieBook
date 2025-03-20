from flask import Blueprint, render_template
from flask_login import current_user
from . import db
from .models import PopularMovies

views = Blueprint("views", __name__)

@views.route('/')
def home():
    result = db.session.execute(db.select(PopularMovies).order_by(PopularMovies.popularity))
    top_movies = result.scalars().all()
    for i in range(len(top_movies)):
        top_movies[i].ranking = len(top_movies) - i
    db.session.commit()
    return render_template('index.html',movies= top_movies ,logged_in= current_user.is_authenticated)