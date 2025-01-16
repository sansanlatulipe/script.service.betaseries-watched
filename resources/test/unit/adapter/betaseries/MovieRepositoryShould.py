import unittest
from unittest import mock
from resources.lib.adapter.betaseries import MovieRepository
from resources.lib.entity import MediumEntity


class MovieRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.betaseries.Http')
    def setUp(self, http):
        self.http = http
        self.config = {}
        self.repo = MovieRepository(self.http, self.config)

    def test_build_movie_when_retrieving_with_known_id(self):
        self.http.get = mock.Mock(return_value=self._buildBsMovieObject(1))

        movie = self.repo.retrieveById(5)

        self.http.get.assert_called_once_with('/movies/movie', {'id': 5})
        self.assertEqual(
            self._buildMovieEntity(True),
            movie
        )

    def test_return_none_when_retrieving_with_unknown_id(self):
        self.http.get = mock.Mock(return_value={})

        movie = self.repo.retrieveById('unknown_id')

        self.http.get.assert_called_once_with('/movies/movie', {'id': 'unknown_id'})
        self.assertIsNone(movie)

    def test_build_movie_when_retrieving_with_known_tmdb_id(self):
        self.http.get = mock.Mock(return_value=self._buildBsMovieObject(0))

        movie = self.repo.retrieveByUniqueId(1005)

        self.http.get.assert_called_once_with('/movies/movie', {'tmdb_id': 1005})
        self.assertEqual(
            self._buildMovieEntity(False),
            movie
        )

    def test_change_movie_status_to_0_when_updating_to_unwatched(self):
        self.config['mail'] = lambda: False
        self.config['twitter'] = lambda: False
        self.config['profile'] = lambda: False
        self.http.post = mock.Mock()

        movie = self._buildMovieEntity(False)
        self.repo.updateWatchedStatus(movie)

        self.http.post.assert_called_once_with('/movies/movie', {
            'id': movie.id,
            'state': 0,
            'mail': 0,
            'twitter': 0,
            'profile': 0
        })

    def test_change_movie_status_to_1_when_updating_to_watched(self):
        self.config['mail'] = lambda: True
        self.config['twitter'] = lambda: True
        self.config['profile'] = lambda: True
        self.http.post = mock.Mock()

        movie = self._buildMovieEntity(True)
        self.repo.updateWatchedStatus(movie)

        self.http.post.assert_called_once_with('/movies/movie', {
            'id': movie.id,
            'state': 1,
            'mail': 1,
            'twitter': 1,
            'profile': 1
        })

    @staticmethod
    def _buildBsMovieObject(status):
        return {
            'movie': {
                'id': 5,
                'tmdb_id': 1005,
                'title': 'Fake movie',
                'user': {
                    'status': status
                }
            }
        }

    @staticmethod
    def _buildMovieEntity(isWatched):
        return MediumEntity(5, 1005, 'Fake movie', isWatched)
