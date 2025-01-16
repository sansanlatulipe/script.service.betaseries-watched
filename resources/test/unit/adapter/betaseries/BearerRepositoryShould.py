import unittest
from unittest import mock
from resources.lib.adapter.betaseries import BearerRepository


class BearerRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.betaseries.Http')
    @mock.patch('resources.lib.adapter.CacheRepository')
    def setUp(self, cache, http):
        self.cache = cache
        self.http = http
        self.repo = BearerRepository(self.cache, self.http)

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
    def test_create_bearer_when_device_token_is_validated(self, patchedTimeSleep):
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
    def test_wait_until_the_token_expires_when_device_is_not_validated(self, patchedTimeSleep):
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
