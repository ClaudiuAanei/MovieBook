from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from . import db
from .models import PopularMovies, PopularSeries, User, RandomMovie
from .forms import RandomMovieForm

views = Blueprint("views", __name__)

@views.route('/')
def home():
    movies_result = db.session.execute(db.select(PopularMovies).order_by(PopularMovies.popularity))
    top_movies = movies_result.scalars().all()[10:]
    for i in range(len(top_movies)):
        top_movies[i].ranking = len(top_movies) - i
    db.session.commit()

    series_result = db.session.execute(db.select(PopularSeries).order_by(PopularSeries.popularity))
    top_series = series_result.scalars().all()
    for i in range(len(top_series)):
        top_series[i].ranking = len(top_series) - i
    db.session.commit()
    return render_template('index.html',movies= top_movies ,series= top_series, logged_in= current_user.is_authenticated)

@views.route('/profile/<user_id>', methods= ['GET', 'POST'])
def show_profile(user_id):
    from .movies_requests import get_random_movie
    form = RandomMovieForm()
    requested_user = db.get_or_404(User, user_id)
    movie = db.session.execute(db.select(RandomMovie).where(current_user.id == RandomMovie.movie_owner)).scalar()
    if form.validate_on_submit():
        year = form.year.data
        category = form.category.data
        try:
            year_u = int(year)
        except ValueError:
            year_u = None
        update_movie = get_random_movie(year= year_u, genre= int(category))
        movie = db.session.execute(db.select(RandomMovie).where(User.id == RandomMovie.movie_owner)).scalar()
        movie.title = update_movie['title']
        movie.overview = update_movie['overview']
        movie.release_date = update_movie['release_date']
        movie.rating = update_movie['rating']
        movie.poster_url = update_movie['poster_url']
        db.session.commit()

        return redirect(url_for('views.show_profile', user_id= current_user.id))

    return render_template('profile.html', logged_in= current_user.is_authenticated,
                               user= requested_user, form= form, movie=movie)