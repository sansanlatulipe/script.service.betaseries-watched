import unittest
from resources.test.mock import patch
from resources.test.mock import MagicMock
from resources.lib.service.movie import WatchSynchro


class WatchSynchroShould(unittest.TestCase):
    @patch('resources.lib.appli.betaseries.MovieRepository')
    @patch('resources.lib.appli.kodi.MovieRepository')
    @patch('resources.lib.appli.cache.Repository')
    def setUp(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo
        self.movie = WatchSynchro(cacheRepo, kodiRepo, bsRepo)

    def test_cache_last_kodi_endpoint_when_the_entire_library_is_scanned(self):
        fakeEndpoint = {'endpoint': 'kodi_endpoint'}
        self.kodiRepo.retrieveUpdatedIdsFrom = MagicMock(return_value=[fakeEndpoint])
        self.cacheRepo.setKodiEndpoint = MagicMock()

        self.movie.scanAll()

        self.kodiRepo.retrieveUpdatedIdsFrom.assert_called_once_with(None, 1)
        self.cacheRepo.setKodiEndpoint.assert_called_once_with(fakeEndpoint.get('endpoint'))

    def test_cache_last_betaseries_endpoint_when_the_entire_library_is_scanned(self):
        fakeEndpoint = {'endpoint': 'betaseries_endpoint'}
        self.bsRepo.retrieveUpdatedIdsFrom = MagicMock(return_value=[fakeEndpoint])
        self.cacheRepo.setBetaseriesEndpoint = MagicMock()

        self.movie.scanAll()

        self.bsRepo.retrieveUpdatedIdsFrom.assert_called_once_with(None, 1)
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with(fakeEndpoint.get('endpoint'))

    def test_reset_cache_endpoints_if_none_exists_when_the_entire_library_is_scanned(self):
        self.kodiRepo.retrieveUpdatedIdsFrom = MagicMock(return_value=[])
        self.bsRepo.retrieveUpdatedIdsFrom = MagicMock(return_value=[])
        self.cacheRepo.setKodiEndpoint = MagicMock()
        self.cacheRepo.setBetaseriesEndpoint = MagicMock()

        self.movie.scanAll()

        self.cacheRepo.setKodiEndpoint.assert_called_once_with(None)
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with(None)
