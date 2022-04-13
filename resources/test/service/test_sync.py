from resources.test.testmod import unittest
from resources.test.testmod import mock
from resources.lib.service.sync import WatchSynchro


class WatchSynchroShould(unittest.TestCase):
    @mock.patch('resources.lib.appli.betaseries.MovieRepository')
    @mock.patch('resources.lib.appli.kodi.MovieRepository')
    @mock.patch('resources.lib.appli.cache.Repository')
    def setUp(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo
        self.sync = WatchSynchro(self.cacheRepo, self.kodiRepo, self.bsRepo)

    def test_cache_last_kodi_endpoint_when_the_entire_library_is_scanned(self):
        fakeEndpoint = {'endpoint': 'event_1'}
        self.kodiRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[fakeEndpoint])
        self.cacheRepo.setKodiEndpoint = mock.Mock()

        self.sync.scanAll()

        self.kodiRepo.retrieveUpdatedIdsFrom.assert_called_once_with(None, 1)
        self.cacheRepo.setKodiEndpoint.assert_called_once_with('event_1')

    def test_cache_last_betaseries_endpoint_when_the_entire_library_is_scanned(self):
        fakeEndpoint = {'endpoint': 'event_1'}
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[fakeEndpoint])
        self.cacheRepo.setBetaseriesEndpoint = mock.Mock()

        self.sync.scanAll()

        self.bsRepo.retrieveUpdatedIdsFrom.assert_called_once_with(None, 1)
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with('event_1')

    def test_reset_cache_endpoints_if_none_exists_when_the_entire_library_is_scanned(self):
        self.kodiRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[])
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[])
        self.cacheRepo.setKodiEndpoint = mock.Mock()
        self.cacheRepo.setBetaseriesEndpoint = mock.Mock()

        self.sync.scanAll()

        self.cacheRepo.setKodiEndpoint.assert_called_once_with(None)
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with(None)

    def test_look_for_all_kodi_media_from_betaseries_when_the_entire_library_is_scanned(self):
        kodiMovies = [
            {'id': 'kodi-1', 'tmdbId': 1001, 'isWatched': False},
            {'id': 'kodi-2', 'tmdbId': 1002, 'isWatched': False}
        ]
        self.kodiRepo.retrieveAll = mock.Mock(return_value=kodiMovies)
        self.bsRepo.retrieveByTmdbId = mock.Mock(return_value=None)

        self.sync.scanAll()

        self.assertEqual(2, self.bsRepo.retrieveByTmdbId.call_count)
        self.bsRepo.retrieveByTmdbId.assert_has_calls([
            mock.call(1001),
            mock.call(1002)
        ])

    def test_mark_betaseries_medium_as_watched_when_it_has_been_watched_on_kodi(self):
        kodiMovie = {'id': 'kodi-1', 'tmdbId': 1001, 'isWatched': True}
        bsMovie = {'id': 'bs-1', 'tmdbId': 1001, 'isWatched': False}
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[kodiMovie])
        self.bsRepo.retrieveByTmdbId = mock.Mock(return_value=bsMovie)
        self.bsRepo.updateWatchedStatus = mock.Mock()

        self.sync.scanAll()

        self.bsRepo.updateWatchedStatus.assert_called_once_with('bs-1', True)

    def test_mark_kodi_medium_as_watched_when_it_has_been_watched_on_betaseries(self):
        kodiMovie = {'id': 'kodi-1', 'tmdbId': 1001, 'isWatched': False}
        bsMovie = {'id': 'bs-1', 'tmdbId': 1001, 'isWatched': True}
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[kodiMovie])
        self.bsRepo.retrieveByTmdbId = mock.Mock(return_value=bsMovie)
        self.kodiRepo.updateWatchedStatus = mock.Mock()

        self.sync.scanAll()

        self.kodiRepo.updateWatchedStatus.assert_called_once_with('kodi-1', True)

    def test_retrieve_kodi_events_from_cached_endpoint_when_scanning_recent_updates(self):
        fakeEndpoint = {'endpoint': 'event_2', 'id': 'kodi-1'}
        self.cacheRepo.getKodiEndpoint = mock.Mock(return_value='event_1')
        self.cacheRepo.setKodiEndpoint = mock.Mock()
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[{'id': 'kodi-1'}])
        self.kodiRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[fakeEndpoint])

        self.sync.scanRecentlyUpdated()

        self.kodiRepo.retrieveUpdatedIdsFrom.assert_called_once_with('event_1')
        self.cacheRepo.setKodiEndpoint.assert_called_once_with('event_2')

    def test_retrieve_betaseries_events_from_cached_endpoint_when_scanning_recent_updates(self):
        fakeEndpoint = {'endpoint': 'event_2', 'id': 'bs-1'}
        self.cacheRepo.getBetaseriesEndpoint = mock.Mock(return_value='event_1')
        self.cacheRepo.setBetaseriesEndpoint = mock.Mock()
        self.bsRepo.retrieveById = mock.Mock(return_value={'id': 'bs-1'})
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[fakeEndpoint])

        self.sync.scanRecentlyUpdated()

        self.bsRepo.retrieveUpdatedIdsFrom.assert_called_once_with('event_1')
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with('event_2')

    def test_update_betaseries_medium_when_its_kodi_twin_has_been_updated_recently(self):
        kodiMovie = {'id': 'kodi-1', 'tmdbId': 1001, 'isWatched': False}
        bsMovie = {'id': 'bs-1', 'tmdbId': 1001, 'isWatched': True}
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[kodiMovie])
        self.bsRepo.retrieveByTmdbId = mock.Mock(return_value=bsMovie)
        self.kodiRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[{'id': 'kodi-1', 'endpoint': 'event_1'}])
        self.bsRepo.updateWatchedStatus = mock.Mock()

        self.sync.scanRecentlyUpdated()

        self.bsRepo.updateWatchedStatus.assert_called_once_with('bs-1', False)

    def test_update_kodi_medium_when_its_betaseries_twin_has_been_updated_recently(self):
        kodiMovie = {'id': 'kodi-1', 'tmdbId': 1001, 'isWatched': True}
        bsMovie = {'id': 'bs-1', 'tmdbId': 1001, 'isWatched': False}
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[kodiMovie])
        self.bsRepo.retrieveById = mock.Mock(return_value=bsMovie)
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[{'id': 'bs-1', 'endpoint': 'event_1'}])
        self.kodiRepo.updateWatchedStatus = mock.Mock()

        self.sync.scanRecentlyUpdated()

        self.kodiRepo.updateWatchedStatus.assert_called_once_with('kodi-1', False)
