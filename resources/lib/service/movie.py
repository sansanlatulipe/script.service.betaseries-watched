class WatchSynchro:
    def __init__(self, cacheRepo, kodiRepo, bsRepo):
        self.cacheRepo = cacheRepo
        self.kodiRepo = kodiRepo
        self.bsRepo = bsRepo

    def scanAll(self):
        self._initializeEndpoint()
        for kodiMovie in self.kodiRepo.retrieveAll():
            bsMovie = self.bsRepo.retrieveByTmdbId(kodiMovie.get('tmdbId'))
            self._synchronizeEntities(kodiMovie, bsMovie, source=None)

    def scanRecentlyUpdated(self):
        kodiMovies = self.kodiRepo.retrieveAll()
        self._scanRecentlyUpdatedOnKodi(kodiMovies)
        self._scanRecentlyUpdatedOnBetaseries(kodiMovies)

    def _scanRecentlyUpdatedOnKodi(self, kodiMovies):
        endpoint = self.cacheRepo.getKodiEndpoint()

        for event in self.kodiRepo.retrieveUpdatedIdsFrom(endpoint):
            endpoint = event.get('endpoint')
            kodiMovie = self._retrieveById(kodiMovies, event.get('movieId'))
            bsMovie = self.bsRepo.retrieveByTmdbId(kodiMovie.get('tmdbId'))
            self._synchronizeEntities(kodiMovie, bsMovie, source='kodi')

        self.cacheRepo.setKodiEndpoint(endpoint)

    def _scanRecentlyUpdatedOnBetaseries(self, kodiMovies):
        endpoint = self.cacheRepo.getBetaseriesEndpoint()

        for event in self.bsRepo.retrieveUpdatedIdsFrom(endpoint):
            endpoint = event.get('endpoint')
            bsMovie = self.bsRepo.retrieveById(event.get('movieId'))
            kodiMovie = self._retrieveByTmdbId(kodiMovies, bsMovie.get('tmdbId'))
            self._synchronizeEntities(kodiMovie, bsMovie, source='betaseries')

        self.cacheRepo.setBetaseriesEndpoint(endpoint)

    def _synchronizeEntities(self, kodiMovie, bsMovie, source):
        if not kodiMovie or not bsMovie or kodiMovie.get('isWatched') == bsMovie.get('isWatched'):
            pass
        elif source == 'kodi' or source is None and kodiMovie.get('isWatched'):
            self.bsRepo.updateWatchedStatus(bsMovie.get('id'), kodiMovie.get('isWatched'))
        elif source == 'betaseries' or source is None and bsMovie.get('isWatched'):
            self.kodiRepo.updateWatchedStatus(kodiMovie.get('id'), bsMovie.get('isWatched'))

    def _initializeEndpoint(self):
        events = self.kodiRepo.retrieveUpdatedIdsFrom(None, 1)
        if events:
            self.cacheRepo.setKodiEndpoint(events[0].get('endpoint'))

        events = self.bsRepo.retrieveUpdatedIdsFrom(None, 1)
        if events:
            self.cacheRepo.setBetaseriesEndpoint(events[0].get('endpoint'))

    def _retrieveById(self, movies, movieId):
        return next(
            (movie for movie in movies if movie.get('id') == movieId),
            None
        )

    def _retrieveByTmdbId(self, movies, tmdbId):
        return next(
            (movie for movie in movies if movie.get('tmdbId') == tmdbId),
            None
        )
