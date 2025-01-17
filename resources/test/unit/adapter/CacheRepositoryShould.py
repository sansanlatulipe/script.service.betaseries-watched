import unittest
from unittest import mock

from resources.lib.adapter import CacheRepository
from resources.lib.infra import SimpleCache


class CacheRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.SimpleCache')
    def setUp(self, cache: SimpleCache) -> None:
        self.cache = cache()
        self.addonId = 'addon.name'
        self.repo = CacheRepository(self.cache, self.addonId)

    def test_retrieve_betaseries_bearer_from_cache(self) -> None:
        expectedBearer = 'expected_bearer'
        self.cache.get.return_value = expectedBearer

        actualBearer = self.repo.getBetaseriesBearer()

        self.cache.get.assert_called_once_with('addon.name.betaseries.token')
        self.assertEqual(expectedBearer, actualBearer)

    def test_store_betaseries_bearer_in_cache(self) -> None:
        expectedBearer = 'expected_bearer'

        self.repo.setBetaseriesBearer(expectedBearer)

        self.cache.set.assert_called_once_with('addon.name.betaseries.token', expectedBearer)

    def test_retrieve_betaseries_endpoint_from_cache(self) -> None:
        expectedEndpoint = 'expected_endpoint'
        self.cache.get.return_value = expectedEndpoint

        actualEndpoint = self.repo.getBetaseriesEndpoint('movie')

        self.cache.get.assert_called_once_with('addon.name.betaseries.movie.endpoint')
        self.assertEqual(expectedEndpoint, actualEndpoint)

    def test_store_betaseries_endpoint_in_cache(self) -> None:
        expectedEndpoint = 'expected_endpoint'

        self.repo.setBetaseriesEndpoint('movie', expectedEndpoint)

        self.cache.set.assert_called_once_with('addon.name.betaseries.movie.endpoint', expectedEndpoint)
