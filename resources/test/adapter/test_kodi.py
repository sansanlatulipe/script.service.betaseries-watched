from resources.test.testmod import unittest
from resources.test.testmod import mock
from resources.lib.adapter.kodi import MovieRepository


class MovieRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.kodi.JsonRPC')
    def setUp(self, jsonrpc):
        self.jsonrpc = jsonrpc
        self.repo = MovieRepository(self.jsonrpc)

    def test_build_movie_when_retrieving_with_known_id(self):
        fakeResponse = {'result': {'moviedetails': self._buildKodiMovieObject(1)}}
        self.jsonrpc.call = mock.Mock(return_value=fakeResponse)

        movie = self.repo.retrieveById(5)

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetMovieDetails',
            {'movieid': 5},
            ['uniqueid', 'playcount']
        )
        self.assertEqual(
            self._buildMovieEntity(True),
            movie
        )

    def test_return_none_when_retrieving_with_unknown_id(self):
        self.jsonrpc.call = mock.Mock(return_value={})

        movie = self.repo.retrieveById('unknown_id')

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetMovieDetails',
            {'movieid': 'unknown_id'},
            ['uniqueid', 'playcount']
        )
        self.assertIsNone(movie)

    def test_build_movies_when_retrieving_all(self):
        fakeResponse = {'result': {'movies': [
            self._buildKodiMovieObject(1),
            self._buildKodiMovieObject(0)
        ]}}
        self.jsonrpc.call = mock.Mock(return_value=fakeResponse)

        movies = self.repo.retrieveAll()

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetMovies',
            {},
            ['uniqueid', 'playcount']
        )
        self.assertEqual(
            [self._buildMovieEntity(True), self._buildMovieEntity(False)],
            movies
        )

    def test_change_movie_playcount_to_0_when_updating_to_unwatched(self):
        self.jsonrpc.call = mock.Mock()

        self.repo.updateWatchedStatus(5, False)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetMovieDetails', {
            'movieid': 5,
            'playcount': 0
        })

    def test_change_movie_playcount_to_1_when_updating_to_watched(self):
        self.jsonrpc.call = mock.Mock()

        self.repo.updateWatchedStatus(5, True)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetMovieDetails', {
            'movieid': 5,
            'playcount': 1
        })

    @staticmethod
    def _buildKodiMovieObject(playcount):
        return {
            'movieid': 5,
            'uniqueid': {
                'tmdb': 1005
            },
            'playcount': playcount
        }

    @staticmethod
    def _buildMovieEntity(isWatched):
        return {
            'id': 5,
            'tmdbId': 1005,
            'isWatched': isWatched
        }
