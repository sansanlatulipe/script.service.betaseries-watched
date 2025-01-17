import unittest
from unittest import mock

from resources.lib.adapter import CacheRepository
from resources.lib.adapter import Logger
from resources.lib.adapter.betaseries import MovieRepository as BsMovieRepository
from resources.lib.adapter.kodi import MovieRepository as KodiMovieRepository
from resources.lib.entity import MediumEntity
from resources.lib.service import WatchSynchro


class WatchSynchroShould(unittest.TestCase):
    @mock.patch('resources.lib.adapter.Logger')
    @mock.patch('resources.lib.adapter.betaseries.MovieRepository')
    @mock.patch('resources.lib.adapter.kodi.MovieRepository')
    @mock.patch('resources.lib.adapter.CacheRepository')
    def setUp(
        self,
        logger: Logger,
        cacheRepo: CacheRepository,
        kodiRepo: KodiMovieRepository,
        bsRepo: BsMovieRepository
    ) -> None:
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo
        self.sync = WatchSynchro(logger, self.cacheRepo, self.kodiRepo, self.bsRepo)

        self.kodiRepo.getKind = mock.Mock(return_value='movie')

    def test_scan_all_when_synchronizing_for_the_first_time(self) -> None:
        self.cacheRepo.getBetaseriesEndpoint = mock.Mock(return_value=None)

        with mock.patch.object(self.sync, 'synchronizeAll') as allMock, \
                mock.patch.object(self.sync, 'synchronizeRecentlyUpdatedOnBetaseries') as updateMock:
            self.sync.synchronize()

        allMock.assert_called_once()
        updateMock.assert_not_called()

    def test_scan_recent_updates_when_not_synchronizing_for_the_first_time(self) -> None:
        self.cacheRepo.getBetaseriesEndpoint = mock.Mock(return_value='event_1')

        with mock.patch.object(self.sync, 'synchronizeAll') as allMock, \
                mock.patch.object(self.sync, 'synchronizeRecentlyUpdatedOnBetaseries') as updateMock:
            self.sync.synchronize()

        allMock.assert_not_called()
        updateMock.assert_called_once()

    def test_cache_last_betaseries_endpoint_when_scanning_whole_library(self) -> None:
        fakeEndpoint = {'endpoint': 'event_1', 'id': 'bs-1'}
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[fakeEndpoint])

        self.sync.synchronizeAll()

        self.bsRepo.retrieveUpdatedIdsFrom.assert_called_once_with(None, 1)
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with('movie', 'event_1')

    def test_reset_cache_endpoints_if_none_exists_when_scanning_whole_library(self) -> None:
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[])

        self.sync.synchronizeAll()

        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with('movie', None)

    def test_look_for_all_kodi_media_from_betaseries_when_scanning_whole_library(self) -> None:
        kodiMovies = [
            self._buildMedium('kodi-1', uniqueId=1001),
            self._buildMedium('kodi-2', uniqueId=1002),
        ]
        self.kodiRepo.retrieveAll = mock.Mock(return_value=kodiMovies)
        self.bsRepo.retrieveByUniqueId = mock.Mock(return_value=None)

        self.sync.synchronizeAll()

        self.assertEqual(2, self.bsRepo.retrieveByUniqueId.call_count)
        self.bsRepo.retrieveByUniqueId.assert_has_calls([
            mock.call(1001),
            mock.call(1002)
        ])

    def test_synchronize_kodi_and_betaseries_media_when_scanning_whole_library(self) -> None:
        kodiMedium = self._buildMedium('kodi-1', isWatched=False)
        bsMedium = self._buildMedium('bs-1', isWatched=False)
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[kodiMedium])
        self.bsRepo.retrieveByUniqueId = mock.Mock(return_value=bsMedium)

        with mock.patch.object(self.sync, 'synchronizeMedia') as syncMock:
            self.sync.synchronizeAll()

        syncMock.assert_called_once_with(kodiMedium, bsMedium)

    def test_retrieve_betaseries_events_from_cached_endpoint_when_scanning_recent_updates(self) -> None:
        fakeEndpoint = {'endpoint': 'event_2', 'id': 'bs-1'}
        self.cacheRepo.getBetaseriesEndpoint = mock.Mock(return_value='event_1')
        self.bsRepo.retrieveById = mock.Mock(return_value=self._buildMedium('bs-1'))
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[fakeEndpoint])

        self.sync.synchronizeRecentlyUpdatedOnBetaseries()

        self.bsRepo.retrieveUpdatedIdsFrom.assert_called_once_with('event_1')
        self.cacheRepo.setBetaseriesEndpoint.assert_called_once_with('movie', 'event_2')

    def test_synchronize_kodi_and_betaseries_media_when_scanning_recent_updates(self) -> None:
        kodiMedium = self._buildMedium('kodi-1', isWatched=False)
        bsMedium = self._buildMedium('bs-1', isWatched=False)
        self.kodiRepo.retrieveAll = mock.Mock(return_value=[kodiMedium])
        self.bsRepo.retrieveById = mock.Mock(return_value=bsMedium)
        self.bsRepo.retrieveUpdatedIdsFrom = mock.Mock(return_value=[{'id': 'bs-1', 'endpoint': 'event_1'}])

        with mock.patch.object(self.sync, 'synchronizeMedia') as syncMock:
            self.sync.synchronizeRecentlyUpdatedOnBetaseries()

        syncMock.assert_called_once_with(kodiMedium, bsMedium, source='betaseries')

    def test_synchronize_kodi_and_betaseries_media_when_adding_medium_on_kodi(self) -> None:
        kodiMedium = self._buildMedium('kodi-1', uniqueId=1001, isWatched=False)
        bsMedium = self._buildMedium('bs-1', isWatched=False)
        self.kodiRepo.retrieveById = mock.Mock(return_value=kodiMedium)
        self.bsRepo.retrieveByUniqueId = mock.Mock(return_value=bsMedium)

        with mock.patch.object(self.sync, 'synchronizeMedia') as syncMock:
            self.sync.synchronizeAddedOnKodi('kodi-1')

        self.kodiRepo.retrieveById.assert_called_once_with('kodi-1')
        self.bsRepo.retrieveByUniqueId.assert_called_once_with(1001)
        syncMock.assert_called_once_with(kodiMedium, bsMedium, source='betaseries')

    def test_synchronize_kodi_and_betaseries_media_when_updating_medium_on_kodi(self) -> None:
        kodiMedium = self._buildMedium('kodi-1', uniqueId=1001, isWatched=False)
        bsMedium = self._buildMedium('bs-1', isWatched=False)
        self.kodiRepo.retrieveById = mock.Mock(return_value=kodiMedium)
        self.bsRepo.retrieveByUniqueId = mock.Mock(return_value=bsMedium)

        with mock.patch.object(self.sync, 'synchronizeMedia') as syncMock:
            self.sync.synchronizeUpdatedOnKodi('kodi-1')

        self.kodiRepo.retrieveById.assert_called_once_with('kodi-1')
        self.bsRepo.retrieveByUniqueId.assert_called_once_with(1001)
        syncMock.assert_called_once_with(kodiMedium, bsMedium, source='kodi')

    def test_not_synchronize_medium_when_betaseries_one_is_missing(self) -> None:
        self.sync.synchronizeMedia(self._buildMedium('kodi-1'), None)

        self.bsRepo.updateWatchedStatus.assert_not_called()
        self.bsRepo.updateWatchedStatus.assert_not_called()

    def test_not_synchronize_medium_when_kodi_one_is_missing(self) -> None:
        self.sync.synchronizeMedia(None, self._buildMedium('bs-1'))

        self.bsRepo.updateWatchedStatus.assert_not_called()
        self.bsRepo.updateWatchedStatus.assert_not_called()

    def test_not_synchronize_media_when_watch_status_are_equal(self) -> None:
        self.sync.synchronizeMedia(
            self._buildMedium('kodi-1', isWatched=True),
            self._buildMedium('bs-1', isWatched=True)
        )
        self.sync.synchronizeMedia(
            self._buildMedium('kodi-2', isWatched=False),
            self._buildMedium('bs-2', isWatched=False)
        )

        self.bsRepo.updateWatchedStatus.assert_not_called()
        self.bsRepo.updateWatchedStatus.assert_not_called()

    def test_update_kodi_medium_when_betaseries_was_watched_on_first_synchronization(self) -> None:
        self.kodiRepo.updateWatchedStatus = mock.Mock()
        kodiMedium = self._buildMedium('kodi-1', isWatched=False)
        bsMedium = self._buildMedium('bs-1', isWatched=True)

        self.sync.synchronizeMedia(kodiMedium, bsMedium)

        self.kodiRepo.updateWatchedStatus.assert_called_once_with(kodiMedium)
        self.assertTrue(kodiMedium.isWatched)

    def test_update_betaseries_medium_when_kodi_was_watched_on_first_synchronization(self) -> None:
        self.bsRepo.updateWatchedStatus = mock.Mock()
        kodiMedium = self._buildMedium('kodi-1', isWatched=True)
        bsMedium = self._buildMedium('bs-1', isWatched=False)

        self.sync.synchronizeMedia(kodiMedium, bsMedium)

        self.bsRepo.updateWatchedStatus.assert_called_once_with(bsMedium)
        self.assertTrue(kodiMedium.isWatched)

    def test_update_kodi_medium_when_watch_status_change_on_betaseries(self) -> None:
        self.kodiRepo.updateWatchedStatus = mock.Mock()
        kodiMedium = self._buildMedium('kodi-1', isWatched=True)
        bsMedium = self._buildMedium('bs-1', isWatched=False)

        self.sync.synchronizeMedia(kodiMedium, bsMedium, source='betaseries')

        self.kodiRepo.updateWatchedStatus.assert_called_once_with(kodiMedium)
        self.assertFalse(kodiMedium.isWatched)

    def test_update_betaseries_medium_when_watch_status_change_on_kodi(self) -> None:
        kodiMedium = self._buildMedium('kodi-1', isWatched=False)
        bsMedium = self._buildMedium('bs-1', isWatched=True)

        self.sync.synchronizeMedia(kodiMedium, bsMedium, source='kodi')

        self.bsRepo.updateWatchedStatus.assert_called_once_with(bsMedium)
        self.assertFalse(bsMedium.isWatched)

    @staticmethod
    def _buildMedium(mediumId: int, uniqueId: int = 1001, isWatched: bool = False) -> MediumEntity:
        return MediumEntity(
            mediumId,
            uniqueId,
            'title',
            isWatched
        )
