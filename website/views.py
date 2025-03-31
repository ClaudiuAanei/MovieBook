from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from . import db
from .models import PopularMovies, PopularSeries, User, RandomMovie, SaveMovie
from .forms import RandomMovieForm
from .movies_requests import get_random_movie, update_popular_movies, update_popular_series

views = Blueprint("views", __name__)

@views.route('/')
def home():
    update_popular_series()
    update_popular_movies()
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

@views.route('/profile/<int:user_id>', methods= ['GET', 'POST'])
def show_profile(user_id):
    form = RandomMovieForm()
    requested_user = db.get_or_404(User, user_id)
    saved_movies = db.session.execute(db.select(SaveMovie).where(SaveMovie.user_who_saved_movie == user_id)).scalars()
    movie = db.session.execute(db.select(RandomMovie).where(RandomMovie.movie_owner == user_id)).scalar()
    if form.validate_on_submit():

        year = form.year.data
        category = form.category.data
        try:
            year_u = int(year)
        except ValueError:
            year_u = None
        update_movie = get_random_movie(year= year_u, genre= int(category))
        if update_movie:
            movie = db.session.execute(db.select(RandomMovie).where(User.id == RandomMovie.movie_owner)).scalar()
            movie.title = update_movie['title']
            movie.overview = update_movie['overview']
            movie.release_date = update_movie['release_date']
            movie.rating = update_movie['rating']
            movie.poster_url = update_movie['poster_url']
            db.session.commit()

            return redirect(url_for('views.show_profile', user_id= current_user.id))

    return render_template('profile.html', logged_in= current_user.is_authenticated,
                               user= requested_user, form= form, movie=movie, saved_movies= saved_movies)
@login_required
@views.route('/add', methods= ['GET','POST'])
def save_movie():
    movie = None
    save_from = request.args.get('save_from')
    print(save_from)
    movie_id = request.args.get('id')
    if save_from == 'profile':
        movie = db.get_or_404(RandomMovie, movie_id)
    elif save_from == 'home':
        movie = db.get_or_404(PopularMovies, movie_id)

    my_movie = SaveMovie(title= movie.title,
                         overview= movie.overview,
                         relase_date= movie.relase_date,
                         rating= movie.rating,
                         poster_url= movie.poster_url,
                         user_who_saved_movie= current_user.id)
    db.session.add(my_movie)
    db.session.commit()


    return redirect(url_for('views.show_profile', user_id= current_user.id))

@views.route('/delete', methods= ['GET', 'POST'])
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(SaveMovie, movie_id)
    if current_user.id == movie_to_delete.user_who_saved_movie:
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for('views.show_profile', user_id= current_user.id))