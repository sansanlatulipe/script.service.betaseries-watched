class MovieRepository:
    def __init__(self, jsonrpc):
        self.jsonrpc = jsonrpc

    def retrieveById(self, movieId):
        response = self.jsonrpc.call(
            'VideoLibrary.GetMovieDetails',
            {'movieid': movieId},
            ['uniqueid', 'playcount']
        )
        return self._buildEntity(response.get('result', {}).get('moviedetails'))

    def retrieveAll(self):
        response = self.jsonrpc.call(
            'VideoLibrary.GetMovies',
            {},
            ['uniqueid', 'playcount']
        )
        return list(map(
            self._buildEntity,
            response.get('result').get('movies')
        ))

    def retrieveUpdatedIdsFrom(self, endpoint, limit=100):
        response = self.jsonrpc.call(
            'VideoLibrary.GetRecentlyAddedMovies',
            {},
            ['dateadded']
        )
        return [
            {
                'id': event.get('movieid'),
                'endpoint': event.get('dateadded')
            } for event in response.get('result').get('movies')[::-1]
        ]

    def updateWatchedStatus(self, movieId, isWatched):
        self.jsonrpc.call(
            'VideoLibrary.SetMovieDetails',
            {
                'movieid': movieId,
                'playcount': 1 if isWatched else 0
            }
        )

    def _buildEntity(self, movie):
        if not movie:
            return None
        return {
            'id': movie.get('movieid'),
            'tmdbId': movie.get('uniqueid').get('tmdb'),
            'isWatched': movie.get('playcount') > 0
        }
