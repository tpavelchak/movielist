import json
import os

from django.test import TestCase

from movies.importers import studio_ghibli


def read_json(rel_path):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, rel_path)
    with open(full_path) as file:
        data = json.loads(file.read())
    return data


class MoviesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.raw_movies_data = read_json('sg_raw_movies_data.json')
        cls.raw_people_data = read_json('sg_raw_people_data.json')

    def _get_simplified_grouped_data(self):
        grouped_data = studio_ghibli.group_movies_data(self.raw_movies_data,
                                                       self.raw_people_data)
        # Simplify grouped data for testing
        simplified_data = {}
        for movie in grouped_data:
            simplified_data[movie['id']] = []
            for person in movie['people']:
                simplified_data[movie['id']].append(person['id'])

        return simplified_data

    def test_grouping_movies_with_people_data(self):
        grouped_data = self._get_simplified_grouped_data()

        people_movies_count = {}
        for person in self.raw_people_data:
            for movie in person['films']:
                movie_id = movie.split('/')[-1]
                people_movies_count[movie_id] = \
                    (people_movies_count[movie_id] + 1
                     if movie_id in people_movies_count else 1)
                self.assertIn(person['id'], grouped_data[movie_id])

        for movie_id, people_count in people_movies_count.items():
            self.assertTrue(len(grouped_data[movie_id]), people_count)

    def test_movies_data_sorting(self):
        grouped_data = studio_ghibli.group_movies_data(self.raw_movies_data,
                                                       self.raw_people_data)
        sorted_movies_title = []
        for movies in grouped_data:
            sorted_movies_title.append(movies['title'])

        movies_title = []
        for movies in self.raw_movies_data:
            movies_title.append(movies['title'])
        movies_title.sort()

        self.assertListEqual(sorted_movies_title, movies_title)

    def test_caching_movies_data(self):
        pass

    def test_backup_movies_data(self):
        pass
