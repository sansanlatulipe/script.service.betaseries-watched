from resources.test.unit.testmod import unittest
from resources.test.unit.testmod import mock
from resources.lib.adapter import kodi


class MovieRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.kodi.JsonRPC')
    def setUp(self, jsonrpc):
        self.jsonrpc = jsonrpc
        self.repo = kodi.MovieRepository(self.jsonrpc)

    def test_build_movie_when_retrieving_with_known_id(self):
        fakeResponse = {'result': {'moviedetails': self._buildMovieObject(1)}}
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
            self._buildMovieObject(1),
            self._buildMovieObject(0)
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

        movie = self._buildMovieEntity(False)
        self.repo.updateWatchedStatus(movie)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetMovieDetails', {
            'movieid': movie.get('id'),
            'playcount': 0
        })

    def test_change_movie_playcount_to_1_when_updating_to_watched(self):
        self.jsonrpc.call = mock.Mock()

        movie = self._buildMovieEntity(True)
        self.repo.updateWatchedStatus(movie)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetMovieDetails', {
            'movieid': movie.get('id'),
            'playcount': 1
        })

    @staticmethod
    def _buildMovieObject(playcount):
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
            'uniqueId': 1005,
            'isWatched': isWatched
        }


class EpisodeRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.kodi.JsonRPC')
    def setUp(self, jsonrpc):
        self.jsonrpc = jsonrpc
        self.repo = kodi.EpisodeRepository(self.jsonrpc)

    def test_build_episode_when_retrieving_with_known_id(self):
        fakeResponse = {'result': {'episodedetails': self._buildEpisodeObject(1)}}
        self.jsonrpc.call = mock.Mock(return_value=fakeResponse)

        episode = self.repo.retrieveById(5)

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetEpisodeDetails',
            {'episodeid': 5},
            ['uniqueid', 'playcount']
        )
        self.assertEqual(
            self._buildEpisodeEntity(True),
            episode
        )

    def test_return_none_when_retrieving_with_unknown_id(self):
        self.jsonrpc.call = mock.Mock(return_value={})

        episode = self.repo.retrieveById('unknown_id')

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetEpisodeDetails',
            {'episodeid': 'unknown_id'},
            ['uniqueid', 'playcount']
        )
        self.assertIsNone(episode)

    def test_build_episodes_when_retrieving_all(self):
        fakeResponse = {'result': {'episodes': [
            self._buildEpisodeObject(1),
            self._buildEpisodeObject(0)
        ]}}
        self.jsonrpc.call = mock.Mock(return_value=fakeResponse)

        episodes = self.repo.retrieveAll()

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetEpisodes',
            {},
            ['uniqueid', 'playcount']
        )
        self.assertEqual(
            [self._buildEpisodeEntity(True), self._buildEpisodeEntity(False)],
            episodes
        )

    def test_change_episode_playcount_to_0_when_updating_to_unwatched(self):
        self.jsonrpc.call = mock.Mock()

        episode = self._buildEpisodeEntity(False)
        self.repo.updateWatchedStatus(episode)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetEpisodeDetails', {
            'episodeid': episode.get('id'),
            'playcount': 0
        })

    def test_change_episode_playcount_to_1_when_updating_to_watched(self):
        self.jsonrpc.call = mock.Mock()

        episode = self._buildEpisodeEntity(True)
        self.repo.updateWatchedStatus(episode)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetEpisodeDetails', {
            'episodeid': episode.get('id'),
            'playcount': 1
        })

    @staticmethod
    def _buildEpisodeObject(playcount):
        return {
            'episodeid': 5,
            'uniqueid': {
                'tvdb': 1005
            },
            'playcount': playcount
        }

    @staticmethod
    def _buildEpisodeEntity(isWatched):
        return {
            'id': 5,
            'uniqueId': 1005,
            'isWatched': isWatched
        }
