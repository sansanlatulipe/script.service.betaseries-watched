class WatchSynchro:
    def __init__(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo

    def scanAll(self):
        self._initializeEndpoint()
        for kodiMovie in self.kodiRepo.retrieveAll():
            bsMovie = self.bsRepo.retrieveByTmdbId(kodiMovie['tmdbId'])
            self._synchronizeEntities(kodiMovie, bsMovie, None)

    def scanRecentlyUpdated(self):
        kodiMovies = self.kodiRepo.retrieveAll()
        self._scanRecentlyUpdatedOnKodi(kodiMovies)
        self._scanRecentlyUpdatedOnBetaseries(kodiMovies)

    def _scanRecentlyUpdatedOnKodi(self, kodiMovies):
        endpoint = self.cacheRepo.getKodiEndpoint()

        for event in self.kodiRepo.retrieveUpdatedIdsFrom(endpoint):
            endpoint = event['endpoint']
            kodiMovie = self._retrieveById(kodiMovies, event['movieId'])
            bsMovie = self.bsRepo.retrieveByTmdbId(kodiMovie['tmdbId'])
            self._synchronizeEntities(kodiMovie, bsMovie, source='kodi')

        self.cacheRepo.setKodiEndpoint(endpoint)

    def _scanRecentlyUpdatedOnBetaseries(self, kodiMovies):
        endpoint = self.cacheRepo.getBetaseriesEndpoint()

        for event in self.bsRepo.retrieveUpdatedIdsFrom(endpoint):
            endpoint = event['endpoint']
            bsMovie = self.bsRepo.retrieveById(event['movieId'])
            kodiMovie = self._retrieveByTmdbId(kodiMovies, bsMovie['tmdbId'])
            self._synchronizeEntities(kodiMovie, bsMovie, source='betaseries')

        self.cacheRepo.setBetaseriesEndpoint(endpoint)

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

    def _retrieveById(self, movies, movieId):
        return next(
            (movie for movie in movies if movie['id'] == movieId),
            None
        )

    def _retrieveByTmdbId(self, movies, tmdbId):
        return next(
            (movie for movie in movies if movie['tmdbId'] == tmdbId),
            None
        )
