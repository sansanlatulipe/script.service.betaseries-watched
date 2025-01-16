from configparser import ConfigParser
from xbmcaddon import Addon
from xbmcgui import Dialog
from xbmcgui import DialogProgressBG
from resources.lib.adapter.kodi import EpisodeRepository as KodiEpisodeRepository
from resources.lib.adapter.kodi import MovieRepository as KodiMovieRepository
from resources.lib.adapter.betaseries import BearerRepository as BsBearerRepository
from resources.lib.adapter.betaseries import EpisodeRepository as BsEpisodeRepository
from resources.lib.adapter.betaseries import MovieRepository as BsMovieRepository
from resources.lib.adapter import CacheRepository
from resources.lib.adapter import Logger
from resources.lib.adapter import Settings
from resources.lib.infra.kodi import JsonRPC as KodiJsonRPC
from resources.lib.infra.betaseries import Http as BsHttp
from resources.lib.infra import SimpleCache
from resources.lib.service import Authentication
from resources.lib.service import Deamon
from resources.lib.service import WatchSynchro


class Container:
    def __init__(self):
        self.singletons = {}

    def get(self, service: str) -> object:
        if service not in self.singletons:
            initializer = '_init' + service.title().replace('.', '')
            self.singletons[service] = getattr(self, initializer)()
        return self.singletons[service]

    def _initAddon(self) -> Addon:
        return Addon()

    def _initAuthentication(self) -> Authentication:
        return Authentication(
            self.get('logger'),
            self.get('betaseries.bearer.repository')
        )

    def _initBetaseriesBearerRepository(self) -> BsBearerRepository:
        return BsBearerRepository(
            self.get('cache.repository'),
            self.get('betaseries.http')
        )

    def _initBetaseriesEpisodeRepository(self) -> BsEpisodeRepository:
        return BsEpisodeRepository(
            self.get('betaseries.http')
        )

    def _initBetaseriesHttp(self) -> BsHttp:
        return BsHttp(
            self.get('settings').getBetaseriesApiKey()
        )

    def _initBetaseriesMovieRepository(self) -> BsMovieRepository:
        return BsMovieRepository(
            self.get('betaseries.http'),
            self.get('settings').getBetaseriesNotifications()
        )

    def _initCacheRepository(self) -> CacheRepository:
        return CacheRepository(
            SimpleCache(),
            self.get('settings').getAddonId()
        )

    def _initDaemonSync(self) -> Deamon:
        return Deamon(
            self.get('settings'),
            self.get('authentication'),
            {
                'movies': self.get('movie.sync'),
                'episodes': self.get('episode.sync')
            }
        )

    def _initEpisodeSync(self) -> WatchSynchro:
        return WatchSynchro(
            self.get('logger'),
            self.get('cache.repository'),
            self.get('kodi.episode.repository'),
            self.get('betaseries.episode.repository')
        )

    def _initKodiEpisodeRepository(self) -> KodiEpisodeRepository:
        return KodiEpisodeRepository(
            self.get('kodi.jsonrpc')
        )

    def _initKodiJsonrpc(self) -> KodiJsonRPC:
        return KodiJsonRPC()

    def _initKodiMovieRepository(self) -> KodiMovieRepository:
        return KodiMovieRepository(
            self.get('kodi.jsonrpc')
        )

    def _initLogger(self) -> Logger:
        return Logger(
            self.get('addon'),
            Dialog,
            DialogProgressBG
        )

    def _initMovieSync(self) -> WatchSynchro:
        return WatchSynchro(
            self.get('logger'),
            self.get('cache.repository'),
            self.get('kodi.movie.repository'),
            self.get('betaseries.movie.repository')
        )

    def _initSettings(self) -> Settings:
        return Settings(
            self.get('addon'),
            ConfigParser()
        )
