import time
import hashlib
from resources.lib.infra import pymod


class MovieRepository:
    def __init__(self, config, http):
        self.config = config
        self.http = http

    def retrieveById(self, movieId):
        response = self.http.call(
            'GET',
            '/movies/movie?' + pymod.urlencode({
                'id': movieId
            })
        )
        return self._buildEntity(response)

    def retrieveByTmdbId(self, tmdbId):
        response = self.http.call(
            'GET',
            '/movies/movie?' + pymod.urlencode({
                'tmdb_id': tmdbId
            })
        )
        return self._buildEntity(response)

    def retrieveUpdatedIdsFrom(self, endpoint, limit=100):
        user = self.http.call('GET', '/members/infos?summary=true')

        params = {
            'types': 'film_add',
            'id': user['member']['id'],
            'nbpp': limit
        }
        if endpoint:
            params['since_id'] = endpoint

        response = self.http.call('GET', '/timeline/member?' + pymod.urlencode(params))
        return [
            {
                'movieId': event['ref_id'],
                'endpoint': event['id']
            } for event in response['events'][::-1]
        ]

    def updateWatchedStatus(self, movieId, isWatched):
        self.http.call(
            'POST',
            '/movies/movie',
            {
                'id': movieId,
                'state': 1 if isWatched else 0,
                'mail': 1 if self.config['notify_mail'] else 0,
                'twitter': 1 if self.config['notify_twitter'] else 0,
                'profile': 1 if self.config['update_profile'] else 0
            }
        )

    def _buildEntity(self, response):
        if 'id' not in response['movie']:
            return None
        return {
            'id': response['movie']['id'],
            'tmdbId': response['movie']['tmdb_id'],
            'isWatched': response['movie']['user']['status'] == 1
        }


class BearerRepository:
    def __init__(self, cacheRepo, http):
        self.http = http
        self.cacheRepo = cacheRepo

    def exists(self):
        bearer = self.cacheRepo.getBetaseriesBearer()
        if bearer:
            self.http.bearer = bearer
            return True
        return False

    def createFromCredentials(self, login, password):
        response = self._initializeFromCredentials(login, password)
        return self._validate(response)

    def createDeviceToken(self):
        return self.http.call('POST', '/oauth/device')

    def createFromDevice(self, device):
        maxRetries = device['expires_in'] // device['interval']
        for retry in range(maxRetries):
            time.sleep(device['interval'])
            response = self._initializeFromDevice(device)
            if self._validate(response):
                return True
        return False

    def _initializeFromCredentials(self, login, password):
        return self.http.call(
            'POST',
            '/members/auth',
            {
                'login': login,
                'password': hashlib.md5(password.encode('utf-8')).hexdigest()
            }
        )

    def _initializeFromDevice(self, device):
        try:
            return self.http.call(
                'POST',
                '/oauth/access_token',
                {
                    'client_id': self.http.clientId,
                    'client_secret': self.http.clientSecret,
                    'code': device['device_code']
                }
            )
        except IOError:
            return {}

    def _validate(self, response):
        if 'access_token' in response:
            self.cacheRepo.setBetaseriesBearer(response['access_token'])
        elif 'token' in response:
            self.cacheRepo.setBetaseriesBearer(response['token'])
        return self.exists()
