class WatchSynchro:
    def __init__(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo

    def scanAll(self):
        self._initializeEndpoint()
        for movieId in self.kodiRepo.retrieveAllIds():
            self._synchronizeByKodiId(movieId, forced=False)

    def scanRecentlyUpdated(self):
        endpoint = self.cacheRepo.getKodiEndpoint()
        for event in self.kodiRepo.retrieveUpdatedIdsFrom(endpoint):
            self._synchronizeByKodiId(event['movieId'], forced=True)
            endpoint = event['endpoint']
        self.cacheRepo.setKodiEndpoint(endpoint)

        endpoint = self.cacheRepo.getBetaseriesEndpoint()
        for event in self.bsRepo.retrieveUpdatedIdsFrom(endpoint):
            self._synchronizeByBetaseriesId(event['movieId'], forced=True)
            endpoint = event['endpoint']
        self.cacheRepo.setBetaseriesEndpoint(endpoint)

    def _synchronizeByKodiId(self, movieId, forced):
        kodiMovie = self.kodiRepo.retrieveById(movieId)
        bsMovie = self.bsRepo.retrieveByTmdbId(kodiMovie['tmdbId'])
        self._synchronizeEntities(kodiMovie, bsMovie, 'kodi' if forced else None)

    def _synchronizeByBetaseriesId(self, movieId, forced):
        bsMovie = self.bsRepo.retrieveById(movieId)
        kodiMovie = self.kodiRepo.retrieveByTmdbId(bsMovie['tmdbId'])
        self._synchronizeEntities(kodiMovie, bsMovie, 'betaseries' if forced else None)

    def _synchronizeEntities(self, kodiMovie, bsMovie, source):
        if kodiMovie is None or bsMovie is None:
            pass
        elif source == 'kodi' and kodiMovie['isWatched'] != bsMovie['isWatched']:
            self.bsRepo.updateWatchedStatus(bsMovie['id'], kodiMovie['isWatched'])
        elif source == 'betaseries' and kodiMovie['isWatched'] != bsMovie['isWatched']:
            self.kodiRepo.updateWatchedStatus(kodiMovie['id'], bsMovie['isWatched'])
        elif kodiMovie['isWatched'] and not bsMovie['isWatched']:
            self.bsRepo.updateWatchedStatus(bsMovie['id'], True)
        elif bsMovie['isWatched'] and not kodiMovie['isWatched']:
            self.kodiRepo.updateWatchedStatus(kodiMovie['id'], True)

    def _initializeEndpoint(self):
        events = self.kodiRepo.retrieveUpdatedIdsFrom(None, 1)
        if events:
            self.cacheRepo.setKodiEndpoint(events[0]['endpoint'])

        events = self.bsRepo.retrieveUpdatedIdsFrom(None, 1)
        if events:
            self.cacheRepo.setBetaseriesEndpoint(events[0]['endpoint'])
