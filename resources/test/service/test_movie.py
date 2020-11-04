from resources.test.testmod import unittest
from resources.test.testmod import mock
from resources.lib.service.movie import WatchSynchro


class WatchSynchroShould(unittest.TestCase):
    @mock.patch('resources.lib.appli.betaseries.MovieRepository')
    @mock.patch('resources.lib.appli.kodi.MovieRepository')
    @mock.patch('resources.lib.appli.cache.Repository')
    def setUp(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo
        self.movie = WatchSynchro(cacheRepo, kodiRepo, bsRepo)

    def test_cache_last_kodi_endpoint_when_the_entire_library_is_scanned(self):
        fakeEndpoint = {'endpoint': 'kodi_endpoint'}
        self.kodiRepo.retrieveUpdatedIdsFrom = mock.MagicMock(return_value=[fakeEndpoint])
        self.cacheRepo.setKodiEndpoint = mock.MagicMock()

        self.movie.scanAll()

        self.kodiRepo.retrieveUpdatedIdsFrom.assert_called_once_with(None, 1)
        self.cacheRepo.setKodiEndpoint.assert_called_once_with(fakeEndpoint.get('endpoint'))

    def test_cache_last_betaseries_endpoint_when_the_entire_library_is_scanned(self):
        fakeEndpoint = {'endpoint': 'betaseries_endpoint'}
        self.bsRepo.retrieveUpdatedIdsFrom = mock.MagicMock(return_value=[fakeEndpoint])
        self.cacheRepo.setBetaseriesEndpoint = mock.MagicMock()

        self.movie.scanAll()

        self.bsRepo.retrieveUpdatedIdsFrom.assert_called_once_with(None, 1)
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with(fakeEndpoint.get('endpoint'))

    def test_reset_cache_endpoints_if_none_exists_when_the_entire_library_is_scanned(self):
        self.kodiRepo.retrieveUpdatedIdsFrom = mock.MagicMock(return_value=[])
        self.bsRepo.retrieveUpdatedIdsFrom = mock.MagicMock(return_value=[])
        self.cacheRepo.setKodiEndpoint = mock.MagicMock()
        self.cacheRepo.setBetaseriesEndpoint = mock.MagicMock()

        self.movie.scanAll()

        self.cacheRepo.setKodiEndpoint.assert_called_once_with(None)
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with(None)
