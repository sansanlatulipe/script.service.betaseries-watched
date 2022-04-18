class Repository:
    def __init__(self, addonId, cache):
        self.addonId = addonId
        self.cache = cache

    def getBetaseriesBearer(self):
        return self.cache.get(self._cacheKey('betaseries.token'))

    def setBetaseriesBearer(self, bearer):
        self.cache.set(self._cacheKey('betaseries.token'), bearer)

    def getBetaseriesEndpoint(self, kind):
        return self.cache.get(self._cacheKey(f'betaseries.{kind}.endpoint'))

    def setBetaseriesEndpoint(self, kind, endpoint):
        self.cache.set(self._cacheKey(f'betaseries.{kind}.endpoint'), endpoint)

    def _cacheKey(self, key):
        return f'{self.addonId}.{key}'
