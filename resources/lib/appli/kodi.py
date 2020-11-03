class MovieRepository:
    def __init__(self, jsonrpc):
        self.jsonrpc = jsonrpc

    def retrieveById(self, movieId):
        response = self.jsonrpc.call(
            'VideoLibrary.GetMovieDetails',
            {'movieid': movieId},
            ['uniqueid', 'playcount']
        )
        return self._buildEntity(response['result']['moviedetails'])

    def retrieveAll(self):
        response = self.jsonrpc.call(
            'VideoLibrary.GetMovies',
            {},
            ['uniqueid', 'playcount']
        )
        return list(map(
            self._buildEntity,
            response['result']['movies']
        ))

    def retrieveUpdatedIdsFrom(self, endpoint, limit=100):
        response = self.jsonrpc.call(
            'VideoLibrary.GetRecentlyAddedMovies',
            {},
            ['dateadded']
        )
        return [
            {
                'movieId': event['movieid'],
                'endpoint': event['dateadded']
            } for event in response['result']['movies'][::-1]
        ]

    def updateWatchedStatus(self, movieId, isWatched):
        self.jsonrpc.call(
            'VideoLibrary.SetMovieDetails',
            {
                'movieid': movieId,
                'playcount': 1 if isWatched else 0
            }
        )

    def _buildEntity(self, data):
        return {
            'id': data['movieid'],
            'tmdbId': data['uniqueid']['tmdb'],
            'isWatched': data['playcount'] > 0
        }
