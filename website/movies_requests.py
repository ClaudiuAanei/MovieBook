import random

from website import db, create_app
import requests
from flask import current_app
from website.models import PopularMovies, PopularSeries
import json
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = create_app()

def update_popular_movies():
    popular_movies = popular_movies_request()
    if len(popular_movies) >= 10:
        with app.app_context():
            db.session.execute(db.delete(PopularMovies))
            db.session.commit()
            for movie in popular_movies:
                if movie['poster_path']:
                    new_movie = PopularMovies(title=movie['title'],
                                          overview=movie['overview'],
                                          poster=MOVIE_DB_IMAGE_URL + movie['poster_path'],
                                          popularity = movie['popularity'],
                                          relase_date=movie['release_date'].split('-')[0])
                    db.session.add(new_movie)
                    db.session.commit()


def popular_movies_request():
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYTkwY2RhNDNhZDc4YmU0OTEwZWZjMGNjOTM1Yjg3MiIsIm5iZiI6MTc0MTI2OTA5Ni44MTIsInN1YiI6IjY3YzlhODY4M2RkN2RhMzk0ZjI0YmI5MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tr43qEjDxnWJslILnvQk6uDIqwo4p-KtXIo6PolgV40"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        url_db_populars = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        re = requests.get(url_db_populars, headers=headers).json()['results']
        popular_movies = sorted(re, key=lambda popular: popular["vote_count"], reverse=True)
        return popular_movies
    else:
        return []

# ===============================================================================================

def update_popular_series():
    popular_series = popular_series_request()
    if len(popular_series) >= 10:
        with app.app_context():
            db.session.execute(db.delete(PopularSeries))
            db.session.commit()
            for serie in popular_series[:10]:
                if serie['poster_path']:
                    new_serie = PopularSeries(title=serie['name'],
                                          overview=serie['overview'],
                                          poster=MOVIE_DB_IMAGE_URL + serie['poster_path'],
                                          popularity = serie['popularity'],
                                          relase_date=serie['first_air_date'].split('-')[0])
                    db.session.add(new_serie)
                    db.session.commit()

def popular_series_request():
    url = "https://api.themoviedb.org/3/trending/tv/day?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYTkwY2RhNDNhZDc4YmU0OTEwZWZjMGNjOTM1Yjg3MiIsIm5iZiI6MTc0MTI2OTA5Ni44MTIsInN1YiI6IjY3YzlhODY4M2RkN2RhMzk0ZjI0YmI5MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tr43qEjDxnWJslILnvQk6uDIqwo4p-KtXIo6PolgV40",
        "language": "en-US"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        popular_series = response.json()['results']
        popular_series = sorted(popular_series, key= lambda popular: popular["first_air_date"], reverse= True)
        return popular_series
    else:
        return []


def get_random_movie(year= None, genre= None):
    url = "https://api.themoviedb.org/3/discover/movie"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYTkwY2RhNDNhZDc4YmU0OTEwZWZjMGNjOTM1Yjg3MiIsIm5iZiI6MTc0MTI2OTA5Ni44MTIsInN1YiI6IjY3YzlhODY4M2RkN2RhMzk0ZjI0YmI5MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tr43qEjDxnWJslILnvQk6uDIqwo4p-KtXIo6PolgV40",
    }
    params = {
        "page": 1,
        "with_original_language": "en"
    }

    if year:
        params['year'] = year
        print(params)

    if genre:
        params['with_genres'] = genre
        print(params)

    random_page = random.randint(1, 10)
    params['page'] = random_page
    print(params)
    response = requests.get(url, headers= headers ,params= params)

    if response.status_code != 200:
        return None

    movies = response.json()['results']
    print(json.dumps(movies, indent= 4))
    random_movie = random.choice(movies)

    return {
        "title": random_movie["title"],
        "overview": random_movie["overview"],
        "release_date": random_movie["release_date"],
        "rating": random_movie["vote_average"],
        "poster_url": f"{MOVIE_DB_IMAGE_URL}{random_movie['poster_path']}"
    }

# series = popular_series_request()
# print(json.dumps(series, indent= 4))
#update_popular_series()

# movies= popular_movies_request()
# print(json.dumps(movies, indent= 4))
#update_popular_movies()
