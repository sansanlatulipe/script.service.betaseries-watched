import unittest
from unittest import mock
from resources.lib.adapter import betaseries


class MovieRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.betaseries.Http')
    def setUp(self, http):
        self.http = http
        self.config = {}
        self.repo = betaseries.MovieRepository(self.http, self.config)

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

    def test_retrieve_last_movie_event_when_retrieving_updates_with_limit_1(self):
        self.http.get = mock.Mock(side_effect=[
            {'member': {'id': 'user_1'}},
            {'events': [{'ref_id': 5, 'id': 12345}]}
        ])

        events = self.repo.retrieveUpdatedIdsFrom(None, 1)

        self.assertEqual(2, self.http.get.call_count)
        self.http.get.assert_called_with('/timeline/member', {
            'types': 'film_add',
            'id': 'user_1',
            'nbpp': 1
        })
        self.assertEqual([{'id': 5, 'endpoint': 12345}], events)

    def test_retrieve_movie_events_when_retrieving_updated_from_endpoint(self):
        self.http.get = mock.Mock(side_effect=[
            {'member': {'id': 'user_1'}},
            {'events': [{'ref_id': 7, 'id': 12347}, {'ref_id': 6, 'id': 12346}]}
        ])

        events = self.repo.retrieveUpdatedIdsFrom(12345)

        self.http.get.assert_called_with('/timeline/member', {
            'types': 'film_add',
            'id': 'user_1',
            'last_id': 12345,
            'nbpp': 100
        })
        self.assertEqual(
            [{'id': 6, 'endpoint': 12346}, {'id': 7, 'endpoint': 12347}],
            events
        )

    def test_change_movie_status_to_0_when_updating_to_unwatched(self):
        self.config['mail'] = lambda: False
        self.config['twitter'] = lambda: False
        self.config['profile'] = lambda: False
        self.http.post = mock.Mock()

        movie = self._buildMovieEntity(False)
        self.repo.updateWatchedStatus(movie)

        self.http.post.assert_called_once_with('/movies/movie', {
            'id': movie.get('id'),
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
            'id': movie.get('id'),
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
        return {
            'id': 5,
            'uniqueId': 1005,
            'title': 'Fake movie',
            'isWatched': isWatched
        }


class EpisodeRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.betaseries.Http')
    def setUp(self, http):
        self.http = http
        self.repo = betaseries.EpisodeRepository(self.http)

    def test_build_episode_when_retrieving_with_known_id(self):
        self.http.get = mock.Mock(return_value=self._buildBsEpisodeObject(True))

        episode = self.repo.retrieveById(5)

        self.http.get.assert_called_once_with('/episodes/display', {'id': 5})
        self.assertEqual(
            self._buildEpisodeEntity(True),
            episode
        )

    def test_return_none_when_retrieving_with_unknown_id(self):
        self.http.get = mock.Mock(return_value={})

        episode = self.repo.retrieveById('unknown_id')

        self.http.get.assert_called_once_with('/episodes/display', {'id': 'unknown_id'})
        self.assertIsNone(episode)

    def test_build_episode_when_retrieving_with_known_tmdb_id(self):
        self.http.get = mock.Mock(return_value=self._buildBsEpisodeObject(False))

        episode = self.repo.retrieveByUniqueId(1005)

        self.http.get.assert_called_once_with('/episodes/display', {'thetvdb_id': 1005})
        self.assertEqual(
            self._buildEpisodeEntity(False),
            episode
        )

    def test_retrieve_last_episode_event_when_retrieving_updates_with_limit_1(self):
        self.http.get = mock.Mock(side_effect=[
            {'member': {'id': 'user_1'}},
            {'events': [{'ref_id': 5, 'id': 12345}]}
        ])

        events = self.repo.retrieveUpdatedIdsFrom(None, 1)

        self.assertEqual(2, self.http.get.call_count)
        self.http.get.assert_called_with('/timeline/member', {
            'types': 'markas',
            'id': 'user_1',
            'nbpp': 1
        })
        self.assertEqual([{'id': 5, 'endpoint': 12345}], events)

    def test_retrieve_episode_events_when_retrieving_updated_from_endpoint(self):
        self.http.get = mock.Mock(side_effect=[
            {'member': {'id': 'user_1'}},
            {'events': [{'ref_id': 7, 'id': 12347}, {'ref_id': 6, 'id': 12346}]}
        ])

        events = self.repo.retrieveUpdatedIdsFrom(12345)

        self.http.get.assert_called_with('/timeline/member', {
            'types': 'markas',
            'id': 'user_1',
            'last_id': 12345,
            'nbpp': 100
        })
        self.assertEqual(
            [{'id': 6, 'endpoint': 12346}, {'id': 7, 'endpoint': 12347}],
            events
        )

    def test_change_episode_status_when_updating_to_unwatched(self):
        self.http.delete = mock.Mock()

        episode = self._buildEpisodeEntity(False)
        self.repo.updateWatchedStatus(episode)

        self.http.delete.assert_called_once_with('/episodes/watched', {
            'id': episode.get('id')
        })

    def test_change_episode_status_when_updating_to_watched(self):
        self.http.post = mock.Mock()

        episode = self._buildEpisodeEntity(True)
        self.repo.updateWatchedStatus(episode)

        self.http.post.assert_called_once_with('/episodes/watched', {
            'id': episode.get('id')
        })

    @staticmethod
    def _buildBsEpisodeObject(seen):
        return {
            'episode': {
                'id': 5,
                'thetvdb_id': 1005,
                'season': 1,
                'episode': 2,
                'show': {
                    'title': 'Fake title'
                },
                'user': {
                    'seen': seen
                }
            }
        }

    @staticmethod
    def _buildEpisodeEntity(isWatched):
        return {
            'id': 5,
            'uniqueId': 1005,
            'title': 'Fake title S01E02',
            'isWatched': isWatched
        }


class BearerRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.betaseries.Http')
    @mock.patch('resources.lib.adapter.cache.Repository')
    def setUp(self, cache, http):
        self.cache = cache
        self.http = http
        self.repo = betaseries.BearerRepository(self.cache, self.http)

        self.http.clientId = 'client_id'
        self.http.clientSecret = 'client_secret'

    def test_retrieve_bearer_from_cache_when_it_exists_and_is_active(self):
        expectedBearer = '98765'
        self.cache.getBetaseriesBearer = mock.Mock(return_value=expectedBearer)

        bearerExists = self.repo.isActive()

        self.http.get.assert_called_once_with('/members/is_active')
        self.assertEqual(expectedBearer, self.http.bearer)
        self.assertTrue(bearerExists)

    def test_return_none_from_cache_when_it_exists_but_has_expired(self):
        expectedBearer = '98765'
        self.cache.getBetaseriesBearer = mock.Mock(side_effect=[
            expectedBearer,
            None
        ])
        self.http.get = mock.Mock(side_effect=IOError())

        bearerExists = self.repo.isActive()

        self.http.get.assert_called_once_with('/members/is_active')
        self.cache.setBetaseriesBearer.assert_called_once_with(None)
        self.assertIsNone(self.http.bearer)
        self.assertIsNone(bearerExists)

    def test_return_none_from_cache_when_bearer_does_not_exist(self):
        self.cache.getBetaseriesBearer = mock.Mock(return_value=None)

        bearerExists = self.repo.isActive()

        self.assertIsNone(self.http.bearer)
        self.assertIsNone(bearerExists)

    def test_return_false_from_cache_when_bearer_does_not_exist_and_use_is_notified(self):
        self.cache.getBetaseriesBearer = mock.Mock(return_value=False)

        bearerExists = self.repo.isActive()

        self.assertFalse(self.http.bearer)
        self.assertFalse(bearerExists)

    def test_create_device_token_when_initializing_authentication(self):
        expectedToken = self._buildDeviceToken()
        self.http.post = mock.Mock(return_value=expectedToken)

        actualToken = self.repo.createDeviceToken()

        self.http.post.assert_called_once_with('/oauth/device')
        self.assertEqual(expectedToken, actualToken)

    @mock.patch('time.sleep', return_value=None)
    def test_create_bearer_when_device_token_is_validated(self, patched_time_sleep):
        device = self._buildDeviceToken()
        expectedBearer = '98765'
        self.http.post = mock.Mock(return_value={'access_token': expectedBearer})
        self.cache.setBetaseriesBearer = mock.Mock()
        self.cache.getBetaseriesBearer = mock.Mock(return_value=expectedBearer)

        authenticated = self.repo.createFromDevice(device)

        self.http.post.assert_called_once_with('/oauth/access_token', self._buildAuthBody())
        self.cache.setBetaseriesBearer.assert_called_once_with(expectedBearer)
        self.assertEqual(expectedBearer, self.http.bearer)
        self.assertTrue(authenticated)

    @mock.patch('time.sleep', return_value=None)
    def test_wait_until_the_token_expires_when_device_is_not_validated(self, patched_time_sleep):
        device = self._buildDeviceToken()
        self.http.post = mock.Mock(side_effect=IOError())
        self.cache.setBetaseriesBearer = mock.Mock()
        self.cache.getBetaseriesBearer = mock.Mock(return_value=None)

        authenticated = self.repo.createFromDevice(device)

        self.assertEqual(2, self.http.post.call_count)
        self.cache.setBetaseriesBearer.assert_called_with(False)
        self.assertFalse(self.http.bearer)
        self.assertFalse(authenticated)

    @staticmethod
    def _buildDeviceToken():
        return {
            'expires_in': 15,
            'interval': 5,
            'device_code': 123456
        }

    def _buildAuthBody(self):
        return {
            'client_id': self.http.clientId,
            'client_secret': self.http.clientSecret,
            'code': 123456
        }
