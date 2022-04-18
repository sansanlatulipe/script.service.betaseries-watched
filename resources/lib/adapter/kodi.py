class MovieRepository:
    def __init__(self, jsonrpc):
        self.jsonrpc = jsonrpc

    @staticmethod
    def getKind():
        return 'movie'

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


class EpisodeRepository:
    def __init__(self, jsonrpc):
        self.jsonrpc = jsonrpc

    @staticmethod
    def getKind():
        return 'episode'

    def retrieveById(self, episodeId):
        response = self.jsonrpc.call(
            'VideoLibrary.GetEpisodeDetails',
            {'episodeid': episodeId},
            ['uniqueid', 'playcount']
        )
        return self._buildEntity(response.get('result', {}).get('episodedetails'))

    def retrieveAll(self):
        response = self.jsonrpc.call(
            'VideoLibrary.GetEpisodes',
            {},
            ['uniqueid', 'playcount']
        )
        return list(map(
            self._buildEntity,
            response.get('result').get('episodes')
        ))

    def updateWatchedStatus(self, episodeId, isWatched):
        self.jsonrpc.call(
            'VideoLibrary.SetEpisodeDetails',
            {
                'episodeid': episodeId,
                'playcount': 1 if isWatched else 0
            }
        )

    def _buildEntity(self, episode):
        if not episode:
            return None
        return {
            'id': episode.get('episodeid'),
            'tmdbId': episode.get('uniqueid').get('tvdb'),
            'isWatched': episode.get('playcount') > 0
        }
