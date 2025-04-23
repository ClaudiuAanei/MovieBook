# utils.py
from flask import request, redirect, url_for, flash
from functools import wraps
from flask_login import current_user
from . import db
from .models import RandomMovie, PopularMovies, PopularSeries, SaveMovie
from .movies_requests import search_movie


def confirmed_user_only(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.confirmation != 1:
            flash('Confirma mail-ul prima data.')
            return redirect(url_for('views.home'))
        return func(*args, **kwargs)
    return decorator


def get_details_by_source(title, source):
    table_map = {
        'randomMovie': RandomMovie,
        'homeMovie': PopularMovies,
        'homeSeries': PopularSeries,
        'saved': SaveMovie
    }
    if source in table_map:
        return db.session.execute(db.select(table_map[source]).where(table_map[source].title == title)).scalar()
    elif source == 'search':
        query = request.args.get('q')
        return get_movie_by_search_title(title, query)
    return None


def get_movie_by_search_title(title, query):
    results = search_movie(query)
    return next((m for m in results if m.title == title), None)


def movie_to_save(save_from, movie_id):
    path = {
        'profile': RandomMovie,
        'movies': PopularMovies,
        'series': PopularSeries,
    }
    if save_from in path:
        return db.get_or_404(path[save_from], movie_id)
    elif save_from == 'search':
        query = request.args.get('q')
        return get_movie_by_search_id(movie_id, query)


def get_movie_by_search_id(movie_id, query):
    results = search_movie(query)
    return next((m for m in results if m.unique_id == int(movie_id)), None)


def special_char(password):
    # special_chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '[', ']', '^', '_', ':', ';', '<', '=', '>', '?', '{', '|', '}']
    # for letter in password:
    #     if letter in special_chars:
    #         return True
    # return False
    special_chars = set(' !"#$%&()*+,-.[]^_:;<=?>{|}')
    return any(char in special_chars for char in password)

if __name__ == '__main__':
    pass
