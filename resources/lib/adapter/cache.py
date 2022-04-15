class Repository:
    def __init__(self, addonId, cache):
        self.prefix = addonId + '.'
        self.cache = cache

    def getBetaseriesBearer(self):
        return self.cache.get(self._cacheKey('betaseries.token'))

    def setBetaseriesBearer(self, bearer):
        self.cache.set(self._cacheKey('betaseries.token'), bearer)

    def getBetaseriesEndpoint(self):
        return self.cache.get(self._cacheKey('betaseries.endpoint'))

    def setBetaseriesEndpoint(self, endpoint):
        self.cache.set(self._cacheKey('betaseries.endpoint'), endpoint)

    def getKodiEndpoint(self):
        return self.cache.get(self._cacheKey('kodi.endpoint'))

    def setKodiEndpoint(self, endpoint):
        self.cache.set(self._cacheKey('kodi.endpoint'), endpoint)

    def _cacheKey(self, key):
        return self.prefix + key
