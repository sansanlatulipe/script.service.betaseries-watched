class MovieRepository:
    def __init__(self, jsonrpc):
        self.jsonrpc = jsonrpc

    def retrieveById(self, movieId):
        response = self.jsonrpc.call(
            'VideoLibrary.GetMovieDetails',
            {'uniqueid': movieId},
            ['tmdb_id', 'playcount']
        )
        return self._buildEntity(response)

    def retrieveByTmdbId(self, tmdbId):
        response = self.jsonrpc.call(
            'VideoLibrary.GetMovieDetails',
            {'tmdb_id': tmdbId},
            ['uniqueid', 'tmdb_id', 'playcount']
        )
        return self._buildEntity(response)

    def retrieveAllIds(self):
        response = self.jsonrpc.call('VideoLibrary.GetMovies')
        return list(map(
            lambda movie: movie['movieid'],
            response['result']['movies']
        ))

    def retrieveUpdatedIdsFrom(self, endpoint, limit=100):
        response = self.jsonrpc.call('VideoLibrary.GetRecentlyAddedMovies')
        return list(map(
            lambda event: {
                'movieId': event['movieid'],
                'endpoint': event['dateadded']
            },
            response['result']['movies']
        ))

    def updateWatchedStatus(self, movieId, isWatched):
        self.jsonrpc.call(
            'VideoLibrary.SetMovieDetails',
            {
                'movieid': movieId,
                'playcount': 1 if isWatched else 0
            }
        )

    def _buildEntity(self, response):
        if 'uniqueid' not in response['result']['moviedetails']:
            return None
        return {
            'id': response['result']['moviedetails']['movieid'],
            'tmdbId': response['result']['moviedetails']['tmdb_id'],
            'isWatched': response['result']['moviedetails']['playcount'] > 0
        }
