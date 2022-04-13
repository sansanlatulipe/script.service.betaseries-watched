class WatchSynchro:
    def __init__(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo

    def scanAll(self):
        for kodiMedium in self.kodiRepo.retrieveAll():
            bsMedium = self.bsRepo.retrieveByTmdbId(kodiMedium.get('tmdbId'))
            self._synchronizeEntities(kodiMedium, bsMedium, source=None)
        self._initializeEndpoints()

    def scanRecentlyUpdated(self):
        kodiMedia = self.kodiRepo.retrieveAll()
        self._scanRecentlyUpdatedOnKodi(kodiMedia)
        self._scanRecentlyUpdatedOnBetaseries(kodiMedia)

    def _scanRecentlyUpdatedOnKodi(self, kodiMedia):
        endpoint = self.cacheRepo.getKodiEndpoint()

        for event in self.kodiRepo.retrieveUpdatedIdsFrom(endpoint):
            endpoint = event.get('endpoint')
            kodiMedium = self._retrieveById(kodiMedia, event.get('id'))
            bsMedium = self.bsRepo.retrieveByTmdbId(kodiMedium.get('tmdbId'))
            self._synchronizeEntities(kodiMedium, bsMedium, source='kodi')

        self.cacheRepo.setKodiEndpoint(endpoint)

    def _scanRecentlyUpdatedOnBetaseries(self, kodiMedia):
        endpoint = self.cacheRepo.getBetaseriesEndpoint()

        for event in self.bsRepo.retrieveUpdatedIdsFrom(endpoint):
            endpoint = event.get('endpoint')
            bsMedium = self.bsRepo.retrieveById(event.get('id'))
            kodiMedium = self._retrieveByTmdbId(kodiMedia, bsMedium.get('tmdbId'))
            self._synchronizeEntities(kodiMedium, bsMedium, source='betaseries')

        self.cacheRepo.setBetaseriesEndpoint(endpoint)

    def _synchronizeEntities(self, kodiMedium, bsMedium, source):
        if not kodiMedium or not bsMedium or kodiMedium.get('isWatched') == bsMedium.get('isWatched'):
            pass
        elif source == 'kodi' or source is None and kodiMedium.get('isWatched'):
            self.bsRepo.updateWatchedStatus(bsMedium.get('id'), kodiMedium.get('isWatched'))
        elif source == 'betaseries' or source is None and bsMedium.get('isWatched'):
            self.kodiRepo.updateWatchedStatus(kodiMedium.get('id'), bsMedium.get('isWatched'))

    def _initializeEndpoints(self):
        events = self.kodiRepo.retrieveUpdatedIdsFrom(None, 1) or [{}]
        self.cacheRepo.setKodiEndpoint(events[0].get('endpoint'))

        events = self.bsRepo.retrieveUpdatedIdsFrom(None, 1) or [{}]
        self.cacheRepo.setBetaseriesEndpoint(events[0].get('endpoint'))

    def _retrieveById(self, Media, id):
        return next(
            (Medium for Medium in Media if Medium.get('id') == id),
            None
        )

    def _retrieveByTmdbId(self, Media, tmdbId):
        return next(
            (Medium for Medium in Media if Medium.get('tmdbId') == tmdbId),
            None
        )
