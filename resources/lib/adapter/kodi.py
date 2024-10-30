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

    def updateWatchedStatus(self, movie):
        self.jsonrpc.call(
            'VideoLibrary.SetMovieDetails',
            {
                'movieid': movie.get('id'),
                'playcount': 1 if movie.get('isWatched') else 0
            }
        )

    def _buildEntity(self, movie):
        if not movie:
            return None
        return {
            'id': movie.get('movieid'),
            'uniqueId': movie.get('uniqueid').get('tmdb'),
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

    def updateWatchedStatus(self, episode):
        self.jsonrpc.call(
            'VideoLibrary.SetEpisodeDetails',
            {
                'episodeid': episode.get('id'),
                'playcount': 1 if episode.get('isWatched') else 0
            }
        )

    def _buildEntity(self, episode):
        if not episode:
            return None
        return {
            'id': episode.get('episodeid'),
            'uniqueId': episode.get('uniqueid').get('tvdb'),
            'isWatched': episode.get('playcount') > 0
        }
