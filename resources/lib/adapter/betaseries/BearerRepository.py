import time

from resources.lib.adapter import CacheRepository
from resources.lib.infra.betaseries import Http


class BearerRepository:
    def __init__(self, cacheRepo: CacheRepository, http: Http) -> None:
        self.cacheRepo = cacheRepo
        self.http = http

    def isActive(self) -> bool | None:
        if self._exists():
            try:
                self.http.get('/members/is_active')
            except IOError:
                self.http.bearer = None
                self.cacheRepo.setBetaseriesBearer(self.http.bearer)
        return self._exists()

    def reset(self) -> None:
        self.http.bearer = False
        self.cacheRepo.setBetaseriesBearer(self.http.bearer)

    def createDeviceToken(self) -> dict:
        return self.http.post('/oauth/device')

    def createFromDevice(self, device: dict) -> bool:
        maxRetries = device.get('expires_in') // device.get('interval') - 1
        for _ in range(maxRetries):
            time.sleep(device.get('interval'))
            response = self._initializeFromDevice(device)
            if self._validate(response):
                return True
        return False

    def _exists(self) -> bool | None:
        self.http.bearer = self.cacheRepo.getBetaseriesBearer()

        if self.http.bearer is None:
            return None

        return self.http.bearer is not False

    def _initializeFromDevice(self, device: dict) -> dict:
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

    def _validate(self, response: dict) -> bool | None:
        bearer = response.get('access_token') or response.get('token') or False
        self.cacheRepo.setBetaseriesBearer(bearer)
        return self._exists()
