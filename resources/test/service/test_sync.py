from resources.test.testmod import unittest
from resources.test.testmod import mock
from resources.lib.service import sync


class DeamonShould(unittest.TestCase):
    @mock.patch('resources.lib.adapter.settings.Settings')
    @mock.patch('resources.lib.infra.kodi.Monitor')
    @mock.patch('resources.lib.adapter.betaseries.BearerRepository')
    @mock.patch('resources.lib.service.sync.WatchSynchro')
    def setUp(self, settings, monitor, authentication, library):
        self.settings = settings
        self.monitor = monitor
        self.authentication = authentication
        self.library = library
        libraries = {'movies': library, 'tvshows': library}
        self.daemon = sync.Deamon(settings, monitor, authentication, libraries)

        self.monitor.abortRequested = mock.Mock(side_effect=[False, True])

    def test_run_while_no_abort_is_requested(self):
        self.monitor.waitForAbort = mock.Mock()

        self.daemon.run()

        self.monitor.waitForAbort.assert_called_once_with(3600)
        self.assertEqual(2, self.monitor.abortRequested.call_count)

    def test_synchronize_every_library_while_running(self):
        self.library.synchronize = mock.Mock()

        self.daemon.run()

        self.assertEqual(2, self.library.synchronize.call_count)

    def test_check_authentication_is_ready_before_synchronizing(self):
        self.authentication.isAuthenticated = mock.Mock(return_value=False)
        self.library.synchronize = mock.Mock()

        self.daemon.run()

        self.assertEqual(2, self.authentication.isAuthenticated.call_count)
        self.library.synchronize.assert_not_called()

    def test_check_can_synchronize_media_kind_before_running_it(self):
        self.settings.canSynchronize = mock.Mock(side_effect=[False, True])
        self.library.synchronize = mock.Mock()

        self.daemon.run()

        self.settings.canSynchronize.assert_has_calls([
            mock.call('movies'),
            mock.call('tvshows')
        ])
        self.library.synchronize.assert_called_once()


class WatchSynchroShould(unittest.TestCase):
    @mock.patch('resources.lib.adapter.betaseries.MovieRepository')
    @mock.patch('resources.lib.adapter.kodi.MovieRepository')
    @mock.patch('resources.lib.adapter.cache.Repository')
    def setUp(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo
        self.sync = sync.WatchSynchro(self.cacheRepo, self.kodiRepo, self.bsRepo)

    def test_scan_all_when_synchronizing_for_the_first_time(self):
        self.cacheRepo.getBetaseriesEndpoint = mock.Mock(return_value=None)

        with mock.patch.object(self.sync, 'scanAll') as allMock, \
                mock.patch.object(self.sync, 'scanRecentlyUpdatedOnBetaseries') as updateMock:
            self.sync.synchronize()

        allMock.assert_called_once()
        updateMock.assert_not_called()

    def test_scan_recent_updates_when_not_synchronizing_for_the_first_time(self):
        self.cacheRepo.getBetaseriesEndpoint = mock.Mock(return_value='event_1')

        with mock.patch.object(self.sync, 'scanAll') as allMock, \
                mock.patch.object(self.sync, 'scanRecentlyUpdatedOnBetaseries') as updateMock:
            self.sync.synchronize()

        allMock.assert_not_called()
        updateMock.assert_called_once()

    def test_cache_last_betaseries_endpoint_when_scanning_whole_library(self):
        fakeEndpoint = {'endpoint': 'event_1', 'id': 'bs-1'}
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[fakeEndpoint])
        self.cacheRepo.setBetaseriesEndpoint = mock.Mock()

        self.sync.scanAll()

        self.bsRepo.retrieveUpdatedIdsFrom.assert_called_once_with(None, 1)
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with('event_1')

    def test_reset_cache_endpoints_if_none_exists_when_scanning_whole_library(self):
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[])
        self.cacheRepo.setBetaseriesEndpoint = mock.Mock()

        self.sync.scanAll()

        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with(None)

    def test_look_for_all_kodi_media_from_betaseries_when_scanning_whole_library(self):
        kodiMovies = [
            self._buildMedium('kodi', '1', tmdbId=1001),
            self._buildMedium('kodi', '2', tmdbId=1002),
        ]
        self.kodiRepo.retrieveAll = mock.Mock(return_value=kodiMovies)
        self.bsRepo.retrieveByTmdbId = mock.Mock(return_value=None)

        self.sync.scanAll()

        self.assertEqual(2, self.bsRepo.retrieveByTmdbId.call_count)
        self.bsRepo.retrieveByTmdbId.assert_has_calls([
            mock.call(1001),
            mock.call(1002)
        ])

    def test_synchronize_kodi_and_betaseries_media_when_scanning_whole_library(self):
        kodiMedium = self._buildMedium('kodi', isWatched=False)
        bsMedium = self._buildMedium('bs', isWatched=False)
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[kodiMedium])
        self.bsRepo.retrieveByTmdbId = mock.Mock(return_value=bsMedium)

        with mock.patch.object(self.sync, 'synchronizeMedia') as syncMock:
            self.sync.scanAll()

        syncMock.assert_called_once_with(kodiMedium, bsMedium)

    def test_retrieve_betaseries_events_from_cached_endpoint_when_scanning_recent_updates(self):
        fakeEndpoint = {'endpoint': 'event_2', 'id': 'bs-1'}
        self.cacheRepo.getBetaseriesEndpoint = mock.Mock(return_value='event_1')
        self.cacheRepo.setBetaseriesEndpoint = mock.Mock()
        self.bsRepo.retrieveById = mock.Mock(return_value={'id': 'bs-1'})
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[fakeEndpoint])

        self.sync.scanRecentlyUpdatedOnBetaseries()

        self.bsRepo.retrieveUpdatedIdsFrom.assert_called_once_with('event_1')
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with('event_2')

    def test_synchronize_kodi_and_betaseries_media_when_scanning_recent_updates(self):
        kodiMedium = self._buildMedium('kodi', isWatched=False)
        bsMedium = self._buildMedium('bs', isWatched=False)
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[kodiMedium])
        self.bsRepo.retrieveById = mock.Mock(return_value=bsMedium)
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[{'id': bsMedium.get('id'), 'endpoint': 'event_1'}])

        with mock.patch.object(self.sync, 'synchronizeMedia') as syncMock:
            self.sync.scanRecentlyUpdatedOnBetaseries()

        syncMock.assert_called_once_with(kodiMedium, bsMedium, source='betaseries')

    def test_not_synchronize_medium_when_betaseries_one_is_missing(self):
        self.bsRepo.updateWatchedStatus = mock.Mock()
        self.kodiRepo.updateWatchedStatus = mock.Mock()

        self.sync.synchronizeMedia(self._buildMedium('kodi'), None)

        self.bsRepo.updateWatchedStatus.assert_not_called()
        self.bsRepo.updateWatchedStatus.assert_not_called()

    def test_not_synchronize_medium_when_kodi_one_is_missing(self):
        self.bsRepo.updateWatchedStatus = mock.Mock()
        self.kodiRepo.updateWatchedStatus = mock.Mock()

        self.sync.synchronizeMedia(None, self._buildMedium('bs'))

        self.bsRepo.updateWatchedStatus.assert_not_called()
        self.bsRepo.updateWatchedStatus.assert_not_called()

    def test_not_synchronize_media_when_watch_status_are_equal(self):
        self.bsRepo.updateWatchedStatus = mock.Mock()
        self.kodiRepo.updateWatchedStatus = mock.Mock()

        self.sync.synchronizeMedia(self._buildMedium('kodi', isWatched=True), self._buildMedium('bs', isWatched=True))
        self.sync.synchronizeMedia(self._buildMedium('kodi', isWatched=False), self._buildMedium('bs', isWatched=False))

        self.bsRepo.updateWatchedStatus.assert_not_called()
        self.bsRepo.updateWatchedStatus.assert_not_called()

    def test_update_kodi_medium_when_betaseries_was_watched_on_first_synchronization(self):
        self.kodiRepo.updateWatchedStatus = mock.Mock()
        kodiMedium = self._buildMedium('kodi', isWatched=False)
        bsMedium = self._buildMedium('bs', isWatched=True)

        self.sync.synchronizeMedia(kodiMedium, bsMedium)

        self.kodiRepo.updateWatchedStatus.assert_called_once_with(kodiMedium.get('id'), True)

    def test_update_betaseries_medium_when_kodi_was_watched_on_first_synchronization(self):
        self.bsRepo.updateWatchedStatus = mock.Mock()
        kodiMedium = self._buildMedium('kodi', isWatched=True)
        bsMedium = self._buildMedium('bs', isWatched=False)

        self.sync.synchronizeMedia(kodiMedium, bsMedium)

        self.bsRepo.updateWatchedStatus.assert_called_once_with('bs-1', True)

    def test_update_kodi_medium_when_watch_status_change_on_betaseries(self):
        self.kodiRepo.updateWatchedStatus = mock.Mock()
        kodiMedium = self._buildMedium('kodi', isWatched=True)
        bsMedium = self._buildMedium('bs', isWatched=False)

        self.sync.synchronizeMedia(kodiMedium, bsMedium, source='betaseries')

        self.kodiRepo.updateWatchedStatus.assert_called_once_with('kodi-1', False)

    def test_update_betaseries_medium_when_watch_status_change_on_kodi(self):
        self.bsRepo.updateWatchedStatus = mock.Mock()
        kodiMedium = self._buildMedium('kodi', isWatched=False)
        bsMedium = self._buildMedium('bs', isWatched=True)

        self.sync.synchronizeMedia(kodiMedium, bsMedium, source='kodi')

        self.bsRepo.updateWatchedStatus.assert_called_once_with('bs-1', False)

    @staticmethod
    def _buildMedium(source, mediumId='1', tmdbId=1001, isWatched=False):
        return {
            'id': source + '-' + mediumId,
            'tmdbId': tmdbId,
            'isWatched': isWatched
        }
