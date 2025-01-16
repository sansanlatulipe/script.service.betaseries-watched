from typing import Union

from resources.lib.infra import SimpleCache


class CacheRepository:
    def __init__(self, cache: SimpleCache, addonId: str) -> None:
        self.cache = cache
        self.addonId = addonId

    def getBetaseriesBearer(self) -> Union[str, False, None]:
        return self.cache.get(self._cacheKey('betaseries.token'))

    def setBetaseriesBearer(self, bearer: Union[str, False, None]) -> None:
        self.cache.set(self._cacheKey('betaseries.token'), bearer)

    def getBetaseriesEndpoint(self, kind: str) -> str | None:
        return self.cache.get(self._cacheKey(f'betaseries.{kind}.endpoint'))

    def setBetaseriesEndpoint(self, kind: str, endpoint: str | None) -> None:
        self.cache.set(self._cacheKey(f'betaseries.{kind}.endpoint'), endpoint)

    def _cacheKey(self, key: str) -> str:
        return f'{self.addonId}.{key}'
