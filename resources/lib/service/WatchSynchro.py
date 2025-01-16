from typing import List
from resources.lib.adapter import MediumRepositoryInterface
from resources.lib.adapter import CacheRepository
from resources.lib.adapter import Logger
from resources.lib.entity import MediumEntity


class WatchSynchro:
    def __init__(
        self,
        logger: Logger,
        cacheRepo: CacheRepository,
        kodiRepo: MediumRepositoryInterface,
        bsRepo: MediumRepositoryInterface
    ):
        self.logger = logger
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo

    def synchronize(self) -> None:
        if not self.isInitialized():
            self.synchronizeAll()
        else:
            self.synchronizeRecentlyUpdatedOnBetaseries()

    def isInitialized(self) -> bool:
        return self.cacheRepo.getBetaseriesEndpoint(self.kodiRepo.getKind()) is not None

    def synchronizeAll(self) -> None:
        self.logger.yellInfo('Starting full synchronization', 21000)

        kodiMedia = self.kodiRepo.retrieveAll()
        mediaCount = len(kodiMedia)

        for mediaProgress, kodiMedium in enumerate(kodiMedia):
            bsMedium = self.bsRepo.retrieveByUniqueId(kodiMedium.uniqueId) or MediumEntity()
            self.synchronizeMedia(kodiMedium, bsMedium)
            self.logger.yellProgress(mediaProgress * 100 // mediaCount, bsMedium.title)
        self._initializeEndpoints()

        self.logger.yellInfo('End of synchronization', 21002)

    def synchronizeRecentlyUpdatedOnBetaseries(self) -> None:
        self.logger.yellInfo('Starting BetaSeries synchronization', 21001)

        endpoint = self.cacheRepo.getBetaseriesEndpoint(self.kodiRepo.getKind())
        kodiMedia = self.kodiRepo.retrieveAll()
        bsEvents = self.bsRepo.retrieveUpdatedIdsFrom(endpoint)
        eventsCount = len(bsEvents)

        for eventsProgress, event in enumerate(bsEvents):
            endpoint = event.get('endpoint')
            bsMedium = self.bsRepo.retrieveById(event.get('id'))
            kodiMedium = self._retrieveByUniqueId(kodiMedia, bsMedium.uniqueId)
            self.synchronizeMedia(kodiMedium, bsMedium, source='betaseries')
            self.logger.yellProgress(eventsProgress * 100 // eventsCount, bsMedium.title)
        self.cacheRepo.setBetaseriesEndpoint(self.kodiRepo.getKind(), endpoint)

        self.logger.yellInfo('End of synchronization', 21002)

    def synchronizeAddedOnKodi(self, kodiId: int) -> None:
        kodiMedium = self.kodiRepo.retrieveById(kodiId)
        bsMedium = self.bsRepo.retrieveByUniqueId(kodiMedium.uniqueId)
        self.synchronizeMedia(kodiMedium, bsMedium, source='betaseries')

        self.logger.yellInfo(bsMedium.title)

    def synchronizeUpdatedOnKodi(self, kodiId: int) -> None:
        kodiMedium = self.kodiRepo.retrieveById(kodiId)
        bsMedium = self.bsRepo.retrieveByUniqueId(kodiMedium.uniqueId)
        self.synchronizeMedia(kodiMedium, bsMedium, source='kodi')

        self.logger.yellInfo(bsMedium.title)

    def synchronizeMedia(self, kodiMedium: MediumEntity, bsMedium: MediumEntity, source: str = None) -> None:
        if self._doestNotNeedToSynchronize(kodiMedium, bsMedium, source):
            pass
        elif self._needsToUpdateBetaseriesMedium(kodiMedium, bsMedium, source):
            bsMedium.isWatched = kodiMedium.isWatched
            self.bsRepo.updateWatchedStatus(bsMedium)
        elif self._needsToUpdateKodiMedium(kodiMedium, bsMedium, source):
            kodiMedium.isWatched = bsMedium.isWatched
            self.kodiRepo.updateWatchedStatus(kodiMedium)

    def _initializeEndpoints(self) -> None:
        events = self.bsRepo.retrieveUpdatedIdsFrom(None, 1) or [{}]
        self.cacheRepo.setBetaseriesEndpoint(self.kodiRepo.getKind(), events[0].get('endpoint'))

    @staticmethod
    def _doestNotNeedToSynchronize(kodiMedium: MediumEntity, bsMedium: MediumEntity, source: str) -> bool:
        return not kodiMedium \
            or not bsMedium \
            or kodiMedium.isWatched == bsMedium.isWatched

    @staticmethod
    def _needsToUpdateBetaseriesMedium(kodiMedium: MediumEntity, bsMedium: MediumEntity, source: str) -> bool:
        return source == 'kodi' \
            or source is None and kodiMedium.isWatched

    @staticmethod
    def _needsToUpdateKodiMedium(kodiMedium: MediumEntity, bsMedium: MediumEntity, source: str) -> bool:
        return source == 'betaseries' \
            or source is None and bsMedium.isWatched

    @staticmethod
    def _retrieveByUniqueId(media: List[MediumEntity], uniqueId: str) -> MediumEntity | None:
        for medium in media:
            if medium.uniqueId == uniqueId:
                return medium
        return None
