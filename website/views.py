# Main for website
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
# Functionality
from . import db
from .models import User, RandomMovie, SaveMovie, Actors
from .forms import RandomMovieForm
from .movies_requests import *
# Exceptions
import sqlite3
from sqlalchemy.exc import IntegrityError

views = Blueprint("views", __name__)
search_result = []

def confirmed_user_only(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.confirmation != 1:
            flash('Confirma mail-ul prima data.')
            return redirect(url_for('views.home'))
        else:
            return func(*args, **kwargs)
    return decorator

@views.route('/', methods= ['GET', 'POST'])
def home():
    global search_result
    search_result = []

    movies_result = db.session.execute(db.select(PopularMovies).order_by(PopularMovies.rating))
    top_movies = movies_result.scalars().all()[::-1]
    for i in range(len(top_movies)):
        top_movies[i].ranking = len(top_movies) - i

    if request.method == 'POST':
        movie = request.form.get('search')
        search_result = search_movie(movie)
    return render_template('index.html',movies= top_movies, results= search_result ,logged_in= current_user.is_authenticated)


@views.route('/profile/<int:user_id>', methods= ['GET', 'POST'])
@login_required
@confirmed_user_only
def show_profile(user_id):
    form = RandomMovieForm()
    requested_user = db.get_or_404(User, user_id)
    saved_movies = db.session.execute(db.select(SaveMovie).where(SaveMovie.user_who_saved_movie == user_id)).scalars().all()
    movie = db.session.execute(db.select(RandomMovie).where(RandomMovie.movie_owner == user_id)).scalar()

    if form.validate_on_submit():
        year = form.year.data
        category = form.category.data

        update_movie = get_random_movie(year= year, genre= int(category))
        if update_movie:
            movie = db.session.execute(db.select(RandomMovie).where(RandomMovie.movie_owner == user_id)).scalar()
            movie.unique_id = update_movie.unique_id
            movie.title = update_movie.title
            movie.overview = update_movie.overview
            movie.poster_url = update_movie.poster_url
            movie.rating = round(update_movie.rating, 2)
            movie.release_date = update_movie.release_date
            movie.trailer = update_movie.trailer

            db.session.commit()

        return redirect(url_for('views.show_profile', user_id= current_user.id))

    return render_template('profile.html', logged_in= current_user.is_authenticated,
                               user= requested_user, form= form, movie=movie, saved_movies= saved_movies)

@views.route("/details/<title>", methods=['GET','POST'])
def see_details(title):
    movie_from = request.args.get('details_from')
    print(movie_from)
    if movie_from == 'randomMovie':
        movie = db.session.execute(db.select(RandomMovie).where(RandomMovie.title == title)).scalar()
        actors = db.session.execute(db.select(Actors).where(Actors.movie_id == movie.unique_id)).scalars().all()
    elif movie_from == 'homeMovie':
        movie = db.session.execute(db.select(PopularMovies).where(PopularMovies.title == title)).scalar()
        actors = db.session.execute(db.select(Actors).where(Actors.movie_id == movie.unique_id)).scalars().all()
    elif movie_from == 'search':
        movie = next((tmovie for tmovie in search_result if tmovie.title == title), None)
        actors = db.session.execute(db.select(Actors).where(Actors.movie_id == movie.unique_id)).scalars().all()
    else:
        movie = db.session.execute(db.select(SaveMovie).where(SaveMovie.title == title)).scalar()
        actors = db.session.execute(db.select(Actors).where(Actors.movie_id == movie.unique_id)).scalars().all()
    if not actors:
        actors_request(movie.unique_id)
        return redirect(url_for('views.see_details', title= title, details_from= movie_from))


    return render_template('details.html', movie= movie, logged_in= current_user.is_authenticated, actors= actors)

@views.route('/add', methods= ['GET','POST'])
@login_required
def save_movie():
    movie = None
    save_from = request.args.get('save_from')
    movie_id = request.args.get('id')
    if save_from == 'profile':
        movie = db.get_or_404(RandomMovie, movie_id)
    elif save_from == 'movies':
        movie = db.get_or_404(PopularMovies, movie_id)
    elif save_from == 'search':
        movie = next((tmovie for tmovie in search_result if tmovie.unique_id == int(movie_id)), None)
    try:
        my_movie = SaveMovie(unique_id = movie.unique_id,
                            title= movie.title,
                            overview= movie.overview,
                            release_date= movie.release_date,
                            rating= round(movie.rating, 2),
                            poster_url= movie.poster_url,
                            trailer= movie.trailer,
                            user_who_saved_movie= current_user.id)
        db.session.add(my_movie)
        db.session.commit()

    except sqlite3.IntegrityError and IntegrityError:
        db.session.rollback()
        flash("This movie is already in your list.")
        return redirect(url_for('views.show_profile', user_id=current_user.id))


    return redirect(url_for('views.show_profile', user_id= current_user.id))


@views.route('/delete', methods= ['GET', 'POST'])
@login_required
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(SaveMovie, movie_id)
    if current_user.id == movie_to_delete.user_who_saved_movie:
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for('views.show_profile', user_id= current_user.id))