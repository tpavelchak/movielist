"""Model uses the Studio Ghibli API to import movies and people.
See https://ghibliapi.herokuapp.com/ for more details.
"""
import requests

from django.core.cache import cache

from . import constants


def get_movies_data():
    """Return imported movies with related to them people.

    Return:
        list: list of a dictionaries representation of movies with people
    """
    # Ensure we have movies data in cache otherwise import the latest
    # movies data and move them to cache on one minute
    movies_data = cache.get(constants.MOVIES_DATA_CACHE_KEY)
    if movies_data is None:
        movies_data = _import_movies_data()

        # Cache
        cache.set(constants.MOVIES_DATA_CACHE_KEY,
                  movies_data,
                  constants.MOVIES_DATA_CACHE_TTL)

    return movies_data


def _import_movies_data():
    """Import movies and people data using Studio Ghibli API.

    Return:
        list: list of a dictionaries representation of movies with people
    """
    # Import movies
    r = requests.get(constants.STUDIO_GHIBLI_API_FILMS_URL)
    movies = r.json()

    # Import people
    r = requests.get(constants.STUDIO_GHIBLI_API_PEOPLE_URL)
    people = r.json()

    # Group people to appropriate movies
    movies_data = {}
    for movie in movies:
        movie['people'] = []
        movies_data[movie['id']] = movie

    for person in people:
        for movie in person['films']:
            movie_id = movie.split('/')[-1]
            movies_data[movie_id]['people'].append(person)

    return list(movies_data.values())

