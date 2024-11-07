import xbmc
from resources.lib.infra.kodi import JsonRPC


class Deamon(xbmc.Monitor):
    def __init__(self, settings, authentication, libraries):
        super().__init__()
        self.settings = settings
        self.authentication = authentication
        self.libraries = libraries

    def run(self):
        while not self.abortRequested():
            for kind in self.libraries.keys():
                if self._isSynchronizationReady(kind):
                    self.libraries.get(kind).synchronize()
            self.waitForAbort(3600)

    def onNotification(self, sender, method, data):
        if method != 'VideoLibrary.OnUpdate':
            return

        data = JsonRPC.decodeResponse(data)
        library = self._retrieveLibraryFromType(data.get('item', {}).get('type', ''))
        mediumId = data.get('item', {}).get('id')
        isNew = data.get('added')

        if not library:
            pass
        elif isNew:
            library.synchronizeAddedOnKodi(mediumId)
        else:
            library.synchronizeUpdatedOnKodi(mediumId)

    def _isSynchronizationReady(self, kind):
        return self.authentication.isAuthenticated() \
            and self.settings.canSynchronize(kind)

    def _retrieveLibraryFromType(self, itemType):
        return self.libraries.get(itemType + 's')


class WatchSynchro:
    def __init__(self, logger, cacheRepo, kodiRepo, bsRepo):
        self.logger = logger
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo

    def synchronize(self):
        if not self.isInitialized():
            self.synchronizeAll()
        else:
            self.synchronizeRecentlyUpdatedOnBetaseries()

    def isInitialized(self):
        return self.cacheRepo.getBetaseriesEndpoint(self.kodiRepo.getKind()) is not None

    def synchronizeAll(self):
        self.logger.yellInfo('Starting full synchronization', 21000)

        kodiMedia = self.kodiRepo.retrieveAll()
        mediaCount = len(kodiMedia)

        for mediaProgress, kodiMedium in enumerate(kodiMedia):
            bsMedium = self.bsRepo.retrieveByUniqueId(kodiMedium.get('uniqueId')) or {}
            self.synchronizeMedia(kodiMedium, bsMedium)
            self.logger.yellProgress(mediaProgress * 100 // mediaCount, bsMedium.get('title'))
        self._initializeEndpoints()

        self.logger.yellInfo('End of synchronization', 21002)

    def synchronizeRecentlyUpdatedOnBetaseries(self):
        self.logger.yellInfo('Starting Betaseries synchronization', 21001)

        endpoint = self.cacheRepo.getBetaseriesEndpoint(self.kodiRepo.getKind())
        kodiMedia = self.kodiRepo.retrieveAll()
        bsEvents = self.bsRepo.retrieveUpdatedIdsFrom(endpoint)
        eventsCount = len(bsEvents)

        for eventsProgress, event in enumerate(bsEvents):
            endpoint = event.get('endpoint')
            bsMedium = self.bsRepo.retrieveById(event.get('id'))
            kodiMedium = self._retrieveByUniqueId(kodiMedia, bsMedium.get('uniqueId'))
            self.synchronizeMedia(kodiMedium, bsMedium, source='betaseries')
            self.logger.yellProgress(eventsProgress * 100 // eventsCount, bsMedium.get('title'))
        self.cacheRepo.setBetaseriesEndpoint(self.kodiRepo.getKind(), endpoint)

        self.logger.yellInfo('End of synchronization', 21002)

    def synchronizeAddedOnKodi(self, kodiId):
        kodiMedium = self.kodiRepo.retrieveById(kodiId)
        bsMedium = self.bsRepo.retrieveByUniqueId(kodiMedium.get('uniqueId'))
        self.synchronizeMedia(kodiMedium, bsMedium, source='betaseries')

        self.logger.yellInfo(bsMedium.get('title'))

    def synchronizeUpdatedOnKodi(self, kodiId):
        kodiMedium = self.kodiRepo.retrieveById(kodiId)
        bsMedium = self.bsRepo.retrieveByUniqueId(kodiMedium.get('uniqueId'))
        self.synchronizeMedia(kodiMedium, bsMedium, source='kodi')

        self.logger.yellInfo(bsMedium.get('title'))

    def synchronizeMedia(self, kodiMedium, bsMedium, source=None):
        if self._doestNotNeedToSynchronize(kodiMedium, bsMedium, source):
            pass
        elif self._needsToUpdateBetaseriesMedium(kodiMedium, bsMedium, source):
            bsMedium['isWatched'] = kodiMedium.get('isWatched')
            self.bsRepo.updateWatchedStatus(bsMedium)
        elif self._needsToUpdateKodiMedium(kodiMedium, bsMedium, source):
            kodiMedium['isWatched'] = bsMedium.get('isWatched')
            self.kodiRepo.updateWatchedStatus(kodiMedium)

    def _initializeEndpoints(self):
        events = self.bsRepo.retrieveUpdatedIdsFrom(None, 1) or [{}]
        self.cacheRepo.setBetaseriesEndpoint(self.kodiRepo.getKind(), events[0].get('endpoint'))

    @staticmethod
    def _doestNotNeedToSynchronize(kodiMedium, bsMedium, source):
        return not kodiMedium \
            or not bsMedium \
            or kodiMedium.get('isWatched') == bsMedium.get('isWatched')

    @staticmethod
    def _needsToUpdateBetaseriesMedium(kodiMedium, bsMedium, source):
        return source == 'kodi' \
            or source is None and kodiMedium.get('isWatched')

    @staticmethod
    def _needsToUpdateKodiMedium(kodiMedium, bsMedium, source):
        return source == 'betaseries' \
            or source is None and bsMedium.get('isWatched')

    @staticmethod
    def _retrieveByUniqueId(media, uniqueId):
        for medium in media:
            if medium.get('uniqueId') == uniqueId:
                return medium
        return None
