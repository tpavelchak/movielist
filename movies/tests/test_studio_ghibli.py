import json
import os
from unittest import mock

from django.core.cache import cache
from django.test import TestCase
import httpretty
import requests

from movies.importers import constants, studio_ghibli


def read_json(rel_path):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, rel_path)
    with open(full_path) as file:
        data = json.loads(file.read())
    return data


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movies_data = read_json('sg_movies_data.json')
        cls.people_data = read_json('sg_people_data.json')

    def get_simplified_grouped_data(self):
        grouped_data = studio_ghibli.group_movies_data(self.movies_data,
                                                       self.people_data)
        # Simplify grouped data for testing
        simplified_data = {}
        for movie in grouped_data:
            simplified_data[movie['id']] = []
            for person in movie['people']:
                simplified_data[movie['id']].append(person['id'])

        return simplified_data

    def test_grouping_movies_with_people_data(self):
        grouped_data = self.get_simplified_grouped_data()

        people_movies_count = {}
        for person in self.people_data:
            for movie in person['films']:
                movie_id = movie.split('/')[-1]
                people_movies_count[movie_id] = \
                    (people_movies_count[movie_id] + 1
                     if movie_id in people_movies_count else 1)
                self.assertIn(person['id'], grouped_data[movie_id])

        for movie_id, people_count in people_movies_count.items():
            self.assertTrue(len(grouped_data[movie_id]), people_count)

    def test_movies_data_sorting(self):
        grouped_data = studio_ghibli.group_movies_data(self.movies_data,
                                                       self.people_data)
        sorted_movies_title = []
        for movies in grouped_data:
            sorted_movies_title.append(movies['title'])

        movies_title = []
        for movies in self.movies_data:
            movies_title.append(movies['title'])
        movies_title.sort()

        self.assertListEqual(sorted_movies_title, movies_title)


class MoviesTestCase(BaseTestCase):
    def setUp(self):
        super(MoviesTestCase, self).setUp()
        cache.clear()
        httpretty.enable()

        self.mock_import_movies_data_response()

    def tearDown(self):
        httpretty.disable()
        super(MoviesTestCase, self).tearDown()

    def mock_import_movies_data_response(self):
        httpretty.register_uri(
            httpretty.GET,
            constants.STUDIO_GHIBLI_API_FILMS_URL,
            content_type='application/json',
            body=json.dumps(self.movies_data)
        )
        httpretty.register_uri(
            httpretty.GET,
            constants.STUDIO_GHIBLI_API_PEOPLE_URL,
            content_type='application/json',
            body=json.dumps(self.people_data)
        )

    def exception_callback(self):
        raise requests.Timeout('Connection timed out.')

    @mock.patch('django.core.cache.cache.get', wraps=cache.get)
    @mock.patch('django.core.cache.cache.set', wraps=cache.set)
    def test_caching_movies_data(self, cache_set_mock, cache_get_mock):
        movies_data = studio_ghibli.get_movies_data()

        # Ensure movies data pushed to cache
        self.assertEqual(cache_get_mock.call_count, 1)
        cache_get_mock.assert_called_with(constants.SG_MOVIES_DATA_CACHE_KEY)
        self.assertEqual(cache_set_mock.call_count, 2)
        cache_set_mock.assert_has_calls([
            mock.call(constants.SG_MOVIES_DATA_CACHE_KEY, movies_data,
                      constants.SG_MOVIES_DATA_CACHE_TTL),
            mock.call(constants.SG_MOVIES_DATA_BACKUP_CACHE_KEY, movies_data,
                      constants.SG_MOVIES_DATA_BACKUP_CACHE_TTL)])

        cache_set_mock.reset_mock()
        cache_get_mock.reset_mock()
        studio_ghibli.get_movies_data()

        # Ensure movies data is returned from the cache
        self.assertEqual(cache_get_mock.call_count, 1)
        cache_get_mock.assert_called_with(constants.SG_MOVIES_DATA_CACHE_KEY)
        self.assertEqual(cache_set_mock.call_count, 0)

    @mock.patch('django.core.cache.cache.get', wraps=cache.get)
    def test_backup_movies_data(self, cache_get_mock):
        # Push movies data into cache
        studio_ghibli.get_movies_data()

        # Remove data for emulating using backup
        cache_get_mock.reset_mock()
        cache.delete(constants.SG_MOVIES_DATA_CACHE_KEY)

        with mock.patch('movies.importers.studio_ghibli.import_movies_data',
                        wraps=self.exception_callback):
            studio_ghibli.get_movies_data()

        self.assertEqual(cache_get_mock.call_count, 2)
        cache_get_mock.assert_called_with(
            constants.SG_MOVIES_DATA_BACKUP_CACHE_KEY)
