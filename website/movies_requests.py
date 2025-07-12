import random
import requests
from website.models import PopularMovies, PopularSeries, Actors
from website import db
import os
from dotenv import find_dotenv, load_dotenv

PATH = find_dotenv()
load_dotenv(PATH)

headers = {
    "accept": "application/json",
    "Authorization": os.getenv("API_MB_TOKEN"),
}

MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

DB = "instance/database_moviebook.db"

session = db.session

def update_popular_movies():
    popular_movies = popular_movies_request()
    if len(popular_movies) >= 10:
        session.query(PopularMovies).delete(synchronize_session=False)
        session.commit()

        new_movies = []
        for movie in popular_movies:
            if movie['poster_path']:
                new_movie = PopularMovies(unique_id= movie['id'],
                                        title=movie['title'],
                                        overview=movie['overview'],
                                        poster_url=MOVIE_DB_IMAGE_URL + movie['poster_path'],
                                        rating = movie['vote_average'],
                                        release_date=movie['release_date'].split('-')[0],
                                        trailer= video_request(movie['id']))
                new_movies.append(new_movie)
        session.bulk_save_objects(new_movies)
        session.commit()


def popular_movies_request():
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        url_db_populars = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        popular_results = requests.get(url_db_populars, headers=headers).json()['results']
        popular_movies = sorted(popular_results, key=lambda popular: popular["vote_count"], reverse=True)
        return popular_movies
    else:
        return []

# ===============================================================================================

def update_popular_series():
    popular_series = popular_series_request()
    if len(popular_series) >= 10:
        session.query(PopularSeries).delete(synchronize_session=False)
        session.commit()

        new_series = []
        for serie in popular_series[:10]:
            if serie['poster_path']:
                new_serie = PopularSeries(unique_id= serie['id'],
                                    title=serie['name'],
                                    overview=serie['overview'],
                                    poster_url=MOVIE_DB_IMAGE_URL + serie['poster_path'],
                                    rating = serie['vote_average'],
                                    release_date=serie['first_air_date'].split('-')[0],
                                    trailer= video_request(serie['id'], True))
                new_series.append(new_serie)
        session.bulk_save_objects(new_series)
        session.commit()

def popular_series_request():
    url = "https://api.themoviedb.org/3/trending/tv/day?language=en-US"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        popular_series = response.json()['results']
        popular_series = sorted(popular_series, key= lambda popular: popular["first_air_date"], reverse= True)
        return popular_series
    else:
        return []

#=======================================================================================================================

class MoviesSearched:
    def __init__(self, id_movie, titles, overview, release_date, rating, poster_path, trailer):
        self.unique_id = id_movie
        self.title = titles
        self.overview = overview
        self.release_date = release_date
        self.rating = rating
        self.poster_url = "https://image.tmdb.org/t/p/w500" + poster_path
        self.trailer = trailer

def get_random_movie(year= None, genre= None):
    url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "page": 1,
        "with_original_language": "en",
        "sort_by": "popularity.desc",
    }
    if year:
        try:
            params['primary_release_year'] = int(year)
        except ValueError:
            params['primary_release_year'] = random.randint(2000, 2025)

    if genre:
        params['with_genres'] = genre

    random_page = random.randint(1, 10)
    params['page'] = random_page
    response = requests.get(url, headers= headers ,params= params)

    if response.status_code != 200:
        return None

    movies = response.json()['results']
    if movies:
        random_movie = random.choice(movies)

        return MoviesSearched(
            random_movie['id'],
            random_movie["title"],
            random_movie['overview'],
            random_movie["release_date"],
            random_movie["vote_average"],
            f"{MOVIE_DB_IMAGE_URL}{random_movie['poster_path']}",
            video_request(random_movie['id'])
        )
    else:
        return None

def search_movie(movie):
    url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"

    params= {
        'query': movie,
    }

    response = requests.get(url, headers= headers, params= params)
    results = response.json()['results']

    results = sorted(results, key= lambda film: film['popularity'], reverse= True)

    movies = []

    for movie in results[:2]:
        movies.append(MoviesSearched(
                       movie['id'],
                       movie['title'],
                       movie['overview'],
                       movie['release_date'],
                       movie['vote_average'],
                       movie['poster_path'],
                       video_request(movie['id'])
                                     )
                      )

    return movies

#=========================================================

def video_request(movie_id, serie= False):
    movie_id = f'{movie_id}'
    if serie:
        url = f"https://api.themoviedb.org/3/tv/{movie_id}/videos"
    else:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        popular_series = response.json()['results']
        for item in popular_series:
            if "Official Trailer" in item['name'] or item['type'] == 'Trailer' and item['official'] == True:
                return f"https://www.youtube.com/embed/{item['key']}"
    else:
        return None

def actors_request(movie_id, serie= False):
    movie_id = f'{movie_id}'
    if serie:
        url = f'https://api.themoviedb.org/3/tv/{movie_id}/credits'
    else:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        actors = []
        credit = response.json()['cast']
        for person in credit[:6]:
            if person['known_for_department'] == 'Acting':
                actor = Actors(actor_name= person['name'],
                               movie_id= movie_id,
                               character= person['character'],
                               profile_picture= "https://image.tmdb.org/t/p/w500" + str(person['profile_path']),
                               popularity= person['popularity'])
                actors.append(actor)
        if actors:
            session.bulk_save_objects(actors)
            session.commit()


if __name__ == '__main__':
    pass
