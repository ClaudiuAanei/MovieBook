# Main for website
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
# Functionality
from . import db
from .models import User, RandomMovie, SaveMovie, Actors
from .forms import RandomMovieForm
from .movies_requests import PopularMovies, PopularSeries, search_movie, get_random_movie, actors_request
from sqlalchemy import and_
from .helpers import confirmed_user_only, get_details_by_source, movie_to_save

views = Blueprint("views", __name__)


@views.route('/', methods= ['GET', 'POST'])
def home():
    if request.method == 'POST':
        movie = request.form.get('search')
        return redirect(url_for('views.home', q=movie))

    query = request.args.get('q')
    search_result = search_movie(query) if query else []

    movies_result = db.session.execute(db.select(PopularMovies).order_by(PopularMovies.rating.desc()))
    top_movies = movies_result.scalars().all()
    for i in range(len(top_movies)):
        top_movies[i].ranking = len(top_movies) - i

    series_result = db.session.execute(db.select(PopularSeries).order_by(PopularSeries.rating.desc()))
    top_series = series_result.scalars().all()
    for i in range(len(top_series)):
        top_series[i].ranking = len(top_series) - i


    return render_template('index.html',movies= top_movies, series= top_series, results= search_result ,logged_in= current_user.is_authenticated)


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
    query = request.args.get('q') if movie_from == 'search' else None
    movie = get_details_by_source(title, movie_from)

    if not movie:
        flash('Nu a fost gasit nici un film cu numele asta')
        return redirect(url_for('views.home'))

    actors = db.session.execute(db.select(Actors).where(Actors.movie_id == movie.unique_id)).scalars().all()
    if not actors:
        for is_series_try in [movie_from == 'homeSeries', True]:
            actors_request(movie.unique_id, is_series_try)
            actors = db.session.execute(
                db.select(Actors).where(Actors.movie_id == movie.unique_id)
            ).scalars().all()
            if actors:
                return redirect(url_for('views.see_details', title=title, details_from=movie_from, q=query))
        flash('Actorii nu au fost găsiți pentru acest titlu.')

    return render_template('details.html', movie= movie, logged_in= current_user.is_authenticated, actors= actors)


@views.route('/add', methods= ['GET','POST'])
@login_required
@confirmed_user_only
def save_movie():
    save_from = request.args.get('save_from')
    movie_id = request.args.get('id')
    movie = movie_to_save(save_from, movie_id)

    if not movie:
        flash("Movie not found.")
        return redirect(url_for('views.show_profile', user_id=current_user.id))

    movie_already_saved = db.session.execute(
        db.select(SaveMovie).where(
            and_(
                SaveMovie.unique_id == movie.unique_id,
                SaveMovie.user_who_saved_movie == current_user.id
            )
        )
    ).scalars().first()

    if movie_already_saved:
        flash(f'"{movie.title}" is already on your list.')
        return redirect(url_for('views.show_profile', user_id= current_user.id))

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
    flash(f'"{movie.title}" is now on your list.')

    return redirect(url_for('views.show_profile', user_id=current_user.id))



@views.route('/delete', methods= ['GET', 'POST'])
@login_required
@confirmed_user_only
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(SaveMovie, movie_id)
    if current_user.id == movie_to_delete.user_who_saved_movie:
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for('views.show_profile', user_id= current_user.id))


