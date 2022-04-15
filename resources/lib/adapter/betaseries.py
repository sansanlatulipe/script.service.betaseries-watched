import time


class MovieRepository:
    def __init__(self, config, http):
        self.config = config
        self.http = http

    def retrieveById(self, movieId):
        response = self.http.get(
            '/movies/movie',
            {'id': movieId}
        )
        return self._buildEntity(response)

    def retrieveByTmdbId(self, tmdbId):
        response = self.http.get(
            '/movies/movie',
            {'tmdb_id': tmdbId}
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
            params['since_id'] = endpoint

        response = self.http.get('/timeline/member', params)
        return [
            {
                'id': event.get('ref_id'),
                'endpoint': event.get('id')
            } for event in response.get('events')[::-1]
        ]

    def updateWatchedStatus(self, movieId, isWatched):
        self.http.post(
            '/movies/movie',
            {
                'id': movieId,
                'state': 1 if isWatched else 0,
                'mail': 1 if self.config.get('notify_mail') else 0,
                'twitter': 1 if self.config.get('notify_twitter') else 0,
                'profile': 1 if self.config.get('update_profile') else 0
            }
        )

    def _buildEntity(self, response):
        if 'id' not in response.get('movie', {}):
            return None
        movie = response.get('movie')
        return {
            'id': movie.get('id'),
            'tmdbId': movie.get('tmdb_id'),
            'isWatched': movie.get('user', {}).get('status') == 1
        }


class BearerRepository:
    def __init__(self, cacheRepo, http):
        self.http = http
        self.cacheRepo = cacheRepo

    def exists(self):
        self.http.bearer = self.cacheRepo.getBetaseriesBearer()
        return self.http.bearer is not None

    def createDeviceToken(self):
        return self.http.post('/oauth/device')

    def createFromDevice(self, device):
        maxRetries = device.get('expires_in') // device.get('interval') - 1
        for retry in range(maxRetries):
            time.sleep(device.get('interval'))
            response = self._initializeFromDevice(device)
            if self._validate(response):
                return True
        return False

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
        bearer = response.get('access_token') or response.get('token')
        self.cacheRepo.setBetaseriesBearer(bearer)
        return self.exists()
