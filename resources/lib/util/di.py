from configparser import ConfigParser
from resources.lib.adapter import kodi as adapterKodi
from resources.lib.adapter import betaseries as adapterBetaseries
from resources.lib.adapter import cache
from resources.lib.adapter import logger
from resources.lib.adapter import settings
from resources.lib.infra import kodi as infraKodi
from resources.lib.infra import betaseries as infraBetaseries
from resources.lib.infra import xbmcmod
from resources.lib.service import authentication
from resources.lib.service import sync


class Container:
    def __init__(self):
        self.singletons = {}
        self.settings = settings.Settings(self.get('addon'), ConfigParser())

    def get(self, service):
        if service not in self.singletons:
            initializer = '_init' + service.title().replace('.', '')
            self.singletons[service] = getattr(self, initializer)()
        return self.singletons[service]

    def _initAddon(self):
        return xbmcmod.Addon()

    def _initAuthentication(self):
        return authentication.Authentication(
            self.get('betaseries.bearer.repository')
        )

    def _initBetaseriesBearerRepository(self):
        return adapterBetaseries.BearerRepository(
            self.get('cache.repository'),
            self.get('betaseries.http')
        )

    def _initBetaseriesEpisodeRepository(self):
        return adapterBetaseries.EpisodeRepository(
            self.get('betaseries.http')
        )

    def _initBetaseriesHttp(self):
        return infraBetaseries.Http(
            self.settings.getBetaseriesApiKey()
        )

    def _initBetaseriesMovieRepository(self):
        return adapterBetaseries.MovieRepository(
            self.settings.getBetaseriesNotifications(),
            self.get('betaseries.http')
        )

    def _initCacheRepository(self):
        return cache.Repository(
            self.settings.getAddonId(),
            xbmcmod.SimpleCache()
        )

    def _initDaemonSync(self):
        return sync.Deamon(
            self.settings,
            self.get('authentication'),
            {
                'movies': self.get('movie.sync'),
                'episodes': self.get('episode.sync')
            }
        )

    def _initEpisodeSync(self):
        return sync.WatchSynchro(
            self.get('logger'),
            self.get('cache.repository'),
            self.get('kodi.episode.repository'),
            self.get('betaseries.episode.repository')
        )

    def _initKodiEpisodeRepository(self):
        return adapterKodi.EpisodeRepository(
            self.get('kodi.jsonrpc')
        )

    def _initKodiJsonrpc(self):
        return infraKodi.JsonRPC()

    def _initKodiMovieRepository(self):
        return adapterKodi.MovieRepository(
            self.get('kodi.jsonrpc')
        )

    def _initLogger(self):
        return logger.Logger(
            self.get('addon'),
            xbmcmod.Dialog,
            xbmcmod.DialogProgressBG
        )

    def _initMovieSync(self):
        return sync.WatchSynchro(
            self.get('logger'),
            self.get('cache.repository'),
            self.get('kodi.movie.repository'),
            self.get('betaseries.movie.repository')
        )
