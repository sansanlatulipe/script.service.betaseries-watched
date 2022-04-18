from resources.lib.infra import xbmcmod
from resources.lib.infra.kodi import JsonRPC


class Deamon(xbmcmod.Monitor):
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
        data = JsonRPC.decodeResponse(data)
        library = self.libraries.get(data.get('type') + 's')
        isNew = data.get('added')

        if method != 'VideoLibrary.OnUpdate' or not library:
            return

        if isNew:
            library.synchronizeAddedOnKodi(data.get('id'))
        else:
            library.synchronizeUpdatedOnKodi(data.get('id'))

    def _isSynchronizationReady(self, kind):
        return self.authentication.isAuthenticated() \
            and self.settings.canSynchronize(kind)


class WatchSynchro:
    def __init__(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo

    def synchronize(self):
        if not self.isInitialized():
            self.synchronizeAll()
        else:
            self.synchronizeRecentlyUpdatedOnBetaseries()

    def isInitialized(self):
        return self.cacheRepo.getBetaseriesEndpoint() is not None

    def synchronizeAll(self):
        for kodiMedium in self.kodiRepo.retrieveAll():
            bsMedium = self.bsRepo.retrieveByTmdbId(kodiMedium.get('tmdbId'))
            self.synchronizeMedia(kodiMedium, bsMedium)
        self._initializeEndpoints()

    def synchronizeRecentlyUpdatedOnBetaseries(self):
        endpoint = self.cacheRepo.getBetaseriesEndpoint()
        kodiMedia = self.kodiRepo.retrieveAll()

        for event in self.bsRepo.retrieveUpdatedIdsFrom(endpoint):
            endpoint = event.get('endpoint')
            bsMedium = self.bsRepo.retrieveById(event.get('id'))
            kodiMedium = self._retrieveByTmdbId(kodiMedia, bsMedium.get('tmdbId'))
            self.synchronizeMedia(kodiMedium, bsMedium, source='betaseries')

        self.cacheRepo.setBetaseriesEndpoint(endpoint)

    def synchronizeAddedOnKodi(self, kodiId):
        kodiMedium = self.kodiRepo.retrieveById(kodiId)
        bsMedium = self.bsRepo.retrieveByTmdbId(kodiMedium.get('tmdbId'))
        self.synchronizeMedia(kodiMedium, bsMedium, source='betaseries')

    def synchronizeUpdatedOnKodi(self, kodiId):
        kodiMedium = self.kodiRepo.retrieveById(kodiId)
        bsMedium = self.bsRepo.retrieveByTmdbId(kodiMedium.get('tmdbId'))
        self.synchronizeMedia(kodiMedium, bsMedium, source='kodi')

    def synchronizeMedia(self, kodiMedium, bsMedium, source=None):
        if self._doestNotNeedToSynchronize(kodiMedium, bsMedium, source):
            pass
        elif self._needsToUpdateBetaseriesMedium(kodiMedium, bsMedium, source):
            self.bsRepo.updateWatchedStatus(bsMedium.get('id'), kodiMedium.get('isWatched'))
        elif self._needsToUpdateKodiMedium(kodiMedium, bsMedium, source):
            self.kodiRepo.updateWatchedStatus(kodiMedium.get('id'), bsMedium.get('isWatched'))

    def _initializeEndpoints(self):
        events = self.bsRepo.retrieveUpdatedIdsFrom(None, 1) or [{}]
        self.cacheRepo.setBetaseriesEndpoint(events[0].get('endpoint'))

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
    def _retrieveByTmdbId(media, tmdbId):
        for medium in media:
            if medium.get('tmdbId') == tmdbId:
                return medium
        return None
