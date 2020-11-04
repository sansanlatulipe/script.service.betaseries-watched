from resources.lib.appli import kodi as appliKodi
from resources.lib.appli import betaseries as appliBetaseries
from resources.lib.appli import cache
from resources.lib.appli import settings
from resources.lib.infra import kodi as infraKodi
from resources.lib.infra import betaseries as infraBetaseries
from resources.lib.infra import pymod
from resources.lib.infra import xbmcmod
from resources.lib.service import authentication
from resources.lib.service import movie


class Container:
    def __init__(self):
        self.singletons = {}
        self.settings = settings.Settings(self.get('addon'), pymod.ConfigParser())

    def get(self, service):
        if service not in self.singletons:
            initializer = '_init' + service.title().replace('.', '')
            self.singletons[service] = getattr(self, initializer)()
        return self.singletons[service]

    def _initAuthentication(self):
        return authentication.Authentication(
            self.get('betaseries.bearer.repository')
        )

    def _initMovieWatch(self):
        return movie.WatchSynchro(
            self.get('cache.repository'),
            self.get('kodi.movie.repository'),
            self.get('betaseries.movie.repository')
        )

    def _initKodiMovieRepository(self):
        return appliKodi.MovieRepository(
            self.get('kodi.jsonrpc')
        )

    def _initBetaseriesMovieRepository(self):
        return appliBetaseries.MovieRepository(
            self.settings.getBetaseriesNotifications(),
            self.get('betaseries.http')
        )

    def _initBetaseriesBearerRepository(self):
        return appliBetaseries.BearerRepository(
            self.get('cache.repository'),
            self.get('betaseries.http')
        )

    def _initCacheRepository(self):
        return cache.Repository(
            self.settings.getAddonId(),
            xbmcmod.SimpleCache()
        )

    def _initKodiJsonrpc(self):
        return infraKodi.JsonRPC()

    def _initBetaseriesHttp(self):
        return infraBetaseries.Http(
            self.settings.getBetaseriesApiKey()
        )

    def _initAddon(self):
        return xbmcmod.Addon()
