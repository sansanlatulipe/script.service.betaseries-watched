import unittest
from unittest import mock

from resources.lib.adapter.kodi import MovieRepository
from resources.lib.entity import MediumEntity
from resources.lib.infra.kodi import JsonRPC


class MovieRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.kodi.JsonRPC')
    def setUp(self, jsonrpc: JsonRPC) -> None:
        self.jsonrpc = jsonrpc
        self.repo = MovieRepository(self.jsonrpc)

    def test_build_movie_when_retrieving_with_known_id(self) -> None:
        fakeResponse = {'result': {'moviedetails': self._buildMovieObject(1)}}
        self.jsonrpc.call = mock.Mock(return_value=fakeResponse)

        movie = self.repo.retrieveById(5)

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetMovieDetails',
            {'movieid': 5},
            ['uniqueid', 'sorttitle', 'playcount']
        )
        self.assertEqual(
            self._buildMovieEntity(True),
            movie
        )

    def test_return_none_when_retrieving_with_unknown_id(self) -> None:
        self.jsonrpc.call = mock.Mock(return_value={})

        movie = self.repo.retrieveById('unknown_id')

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetMovieDetails',
            {'movieid': 'unknown_id'},
            ['uniqueid', 'sorttitle', 'playcount']
        )
        self.assertIsNone(movie)

    def test_build_movies_when_retrieving_all(self) -> None:
        fakeResponse = {'result': {'movies': [
            self._buildMovieObject(1),
            self._buildMovieObject(0)
        ]}}
        self.jsonrpc.call = mock.Mock(return_value=fakeResponse)

        movies = self.repo.retrieveAll()

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetMovies',
            {},
            ['uniqueid', 'sorttitle', 'playcount']
        )
        self.assertEqual(
            [self._buildMovieEntity(True), self._buildMovieEntity(False)],
            movies
        )

    def test_change_movie_playcount_to_0_when_updating_to_unwatched(self) -> None:
        movie = self._buildMovieEntity(False)
        self.repo.updateWatchedStatus(movie)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetMovieDetails', {
            'movieid': movie.id,
            'playcount': 0
        })

    def test_change_movie_playcount_to_1_when_updating_to_watched(self) -> None:
        movie = self._buildMovieEntity(True)
        self.repo.updateWatchedStatus(movie)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetMovieDetails', {
            'movieid': movie.id,
            'playcount': 1
        })

    @staticmethod
    def _buildMovieObject(playcount: int) -> dict:
        return {
            'movieid': 5,
            'uniqueid': {
                'tmdb': 1005
            },
            'sorttitle': 'Movie title',
            'playcount': playcount
        }

    @staticmethod
    def _buildMovieEntity(isWatched: bool) -> MediumEntity:
        return MediumEntity(5, 1005, 'Movie title', isWatched)
