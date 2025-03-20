import json

from website import db, create_app
from flask import current_app
from website.models import PopularMovies
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
app = create_app()
def update_popular_movies():
    import requests
    url = "https://api.themoviedb.org/3/authentication"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYTkwY2RhNDNhZDc4YmU0OTEwZWZjMGNjOTM1Yjg3MiIsIm5iZiI6MTc0MTI2OTA5Ni44MTIsInN1YiI6IjY3YzlhODY4M2RkN2RhMzk0ZjI0YmI5MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tr43qEjDxnWJslILnvQk6uDIqwo4p-KtXIo6PolgV40"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        url_db_populars = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
        re = requests.get(url_db_populars, headers= headers).json()['results']
        with app.app_context():
            for movie in re[:10]:
                if movie['poster_path']:
                    new_movie = PopularMovies(title=movie['title'],
                                          overview=movie['overview'],
                                          poster=MOVIE_DB_IMAGE_URL + movie['poster_path'],
                                          popularity = movie['popularity'],
                                          relase_date=movie['release_date'].split('-')[0])
                    db.session.add(new_movie)
                    db.session.commit()


update_popular_movies()