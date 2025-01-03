import time


class MovieRepository:
    def __init__(self, http, config):
        self.http = http
        self.config = config

    def retrieveById(self, movieId):
        response = self.http.get(
            '/movies/movie',
            {'id': movieId}
        )
        return self._buildEntity(response)

    def retrieveByUniqueId(self, uniqueId):
        response = self.http.get(
            '/movies/movie',
            {'tmdb_id': uniqueId}
        )
        return self._buildEntity(response)

    def retrieveUpdatedIdsFrom(self, endpoint, limit=100):
        user = self.http.get('/members/infos', {'summary': 'true'})

        params = {
            'types': 'film_add',
            'id': user.get('member').get('id'),
            'nbpp': limit
        }
        if endpoint:
            params['last_id'] = endpoint

        response = self.http.get('/timeline/member', params)
        return [
            {
                'id': event.get('ref_id'),
                'endpoint': event.get('id')
            } for event in response.get('events')[::-1]
        ]

    def updateWatchedStatus(self, movie):
        self.http.post(
            '/movies/movie',
            {
                'id': movie.get('id'),
                'state': 1 if movie.get('isWatched') else 0,
                'mail': 1 if self.config.get('mail')() else 0,
                'twitter': 1 if self.config.get('twitter')() else 0,
                'profile': 1 if self.config.get('profile')() else 0
            }
        )

    def _buildEntity(self, response):
        if 'id' not in response.get('movie', {}):
            return None

        movie = response.get('movie')

        return {
            'id': movie.get('id'),
            'uniqueId': movie.get('tmdb_id'),
            'title': movie.get('title'),
            'isWatched': movie.get('user', {}).get('status') == 1
        }


class EpisodeRepository:
    def __init__(self, http):
        self.http = http

    def retrieveById(self, episodeId):
        response = self.http.get(
            '/episodes/display',
            {'id': episodeId}
        )
        return self._buildEntity(response)

    def retrieveByUniqueId(self, uniqueId):
        response = self.http.get(
            '/episodes/display',
            {'thetvdb_id': uniqueId}
        )
        return self._buildEntity(response)

    def retrieveUpdatedIdsFrom(self, endpoint, limit=100):
        user = self.http.get('/members/infos', {'summary': 'true'})

        params = {
            'types': 'markas',
            'id': user.get('member').get('id'),
            'nbpp': limit
        }
        if endpoint:
            params['last_id'] = endpoint

        response = self.http.get('/timeline/member', params)
        return [
            {
                'id': event.get('ref_id'),
                'endpoint': event.get('id')
            } for event in response.get('events')[::-1]
        ]

    def updateWatchedStatus(self, episode):
        method = self.http.post if episode.get('isWatched') else self.http.delete
        method(
            '/episodes/watched',
            {'id': episode.get('id')}
        )

    def _buildEntity(self, response):
        if 'id' not in response.get('episode', {}):
            return None

        episode = response.get('episode')
        showTitle = episode.get('show', {}).get('title')
        seasonNumber = episode.get('season')
        episodeNumber = episode.get('episode')

        return {
            'id': episode.get('id'),
            'uniqueId': episode.get('thetvdb_id'),
            'title': f'{showTitle} S{seasonNumber:02d}E{episodeNumber:02d}',
            'isWatched': episode.get('user', {}).get('seen', False)
        }


class BearerRepository:
    def __init__(self, cacheRepo, http):
        self.http = http
        self.cacheRepo = cacheRepo

    def isActive(self):
        if self._exists():
            try:
                self.http.get('/members/is_active')
            except IOError:
                self.http.bearer = None
                self.cacheRepo.setBetaseriesBearer(self.http.bearer)
        return self._exists()

    def reset(self):
        self.http.bearer = False
        self.cacheRepo.setBetaseriesBearer(self.http.bearer)

    def createDeviceToken(self):
        return self.http.post('/oauth/device')

    def createFromDevice(self, device):
        maxRetries = device.get('expires_in') // device.get('interval') - 1
        for _ in range(maxRetries):
            time.sleep(device.get('interval'))
            response = self._initializeFromDevice(device)
            if self._validate(response):
                return True
        return False

    def _exists(self):
        self.http.bearer = self.cacheRepo.getBetaseriesBearer()

        if self.http.bearer is None:
            return None

        return self.http.bearer is not False

    def _initializeFromDevice(self, device):
        try:
            return self.http.post(
                '/oauth/access_token',
                {
                    'client_id': self.http.clientId,
                    'client_secret': self.http.clientSecret,
                    'code': device.get('device_code')
                }
            )
        except IOError:
            return {}

    def _validate(self, response):
        bearer = response.get('access_token') or response.get('token') or False
        self.cacheRepo.setBetaseriesBearer(bearer)
        return self._exists()
