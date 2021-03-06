"""Model uses the Studio Ghibli API to import movies and people.

See https://ghibliapi.herokuapp.com/ for more details.
"""
from django.core.cache import cache
import requests

from . import constants


def get_movies_data():
    """Return imported movies with related to them people.

    Return:
        list: list of a dictionaries representation of movies with people
    """
    # Ensure we have movies data in cache otherwise import the latest
    # movies data and move them to cache on one minute
    movies_data = cache.get(constants.SG_MOVIES_DATA_CACHE_KEY)
    if movies_data is None:
        try:
            imported_raw_data = import_movies_data()
        except Exception as e:
            # Ensure we have backup otherwise raise exception
            backup = cache.get(constants.SG_MOVIES_DATA_BACKUP_CACHE_KEY)
            if backup is None:
                raise e
            movies_data = backup
            cache.set(constants.SG_MOVIES_DATA_CACHE_KEY,
                      movies_data,
                      constants.SG_MOVIES_DATA_CACHE_TTL)
        else:
            movies_data = group_movies_data(*imported_raw_data)
            cache.set(constants.SG_MOVIES_DATA_CACHE_KEY,
                      movies_data,
                      constants.SG_MOVIES_DATA_CACHE_TTL)

            # Backup movies data on 24 hours just in case
            cache.set(constants.SG_MOVIES_DATA_BACKUP_CACHE_KEY,
                      movies_data,
                      constants.SG_MOVIES_DATA_BACKUP_CACHE_TTL)

    return movies_data


def group_movies_data(movies, people):
    """Map people to appropriate movies.

    Return:
        list: list of a dictionaries representation of movies with people
    """
    # Map people to appropriate movies
    movies_data = {}
    for movie in movies:
        movie['people'] = []
        movies_data[movie['id']] = movie

    for person in people:
        for movie in person['films']:
            movie_id = movie.split('/')[-1]
            movies_data[movie_id]['people'].append(person)

    return sorted(list(movies_data.values()), key=lambda m: m['title'])


def import_movies_data():
    """Import movies and people data using Studio Ghibli API.

    Return:
        tuple: `(movies, people)` raw movies and people data
    """
    # Import movies
    r = requests.get(constants.STUDIO_GHIBLI_API_FILMS_URL)
    movies = r.json()

    # Import people
    r = requests.get(constants.STUDIO_GHIBLI_API_PEOPLE_URL)
    people = r.json()

    return movies, people
