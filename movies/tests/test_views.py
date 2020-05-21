from django.test import TestCase
from django.urls import reverse


class MoviesIndexViewTestCase(TestCase):
    def test_get_movies(self):
        response = self.client.get(reverse('movies:index'))
        self.assertEqual(response.status_code, 200)
