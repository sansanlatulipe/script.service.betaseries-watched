# pylint: disable=no-self-use

from resources.lib.appli import kodi as appliKodi
from resources.lib.appli import betaseries as appliBetaseries
from resources.lib.appli import cache
from resources.lib.infra import kodi as infraKodi
from resources.lib.infra import betaseries as infraBetaseries
from resources.lib.infra import pymod
from resources.lib.infra import xbmcmod
from resources.lib.service import authentication
from resources.lib.service import movie


class Container:
    def __init__(self):
        self.config = pymod.ConfigParser()
        self.config.read('resources/data/config.ini')
        self.addon = xbmcmod.Addon()
        self.singletons = {}

    def get(self, service):
        if service not in self.singletons:
            initializer = '_init' + service.title().replace('.', '')
            self.singletons[service] = getattr(self, initializer)()
        return self.singletons[service]

    def _initAuthentication(self):
        if self.addon.getSetting('bs_login') and self.addon.getSetting('bs_password'):
            config = {
                'login': self.addon.getSetting('bs_login'),
                'password': self.addon.getSetting('bs_password')
            }
        else:
            config = {}
        return authentication.Authentication(
            config,
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
        config = {
            'notify_mail': self.addon.getSetting('notify_mail') == 'true',
            'notify_twitter': self.addon.getSetting('notify_twitter') == 'true',
            'update_profile': self.addon.getSetting('update_profile') == 'true'
        }
        return appliBetaseries.MovieRepository(
            config,
            self.get('betaseries.http')
        )

    def _initBetaseriesBearerRepository(self):
        return appliBetaseries.BearerRepository(
            self.get('cache.repository'),
            self.get('betaseries.http')
        )

    def _initCacheRepository(self):
        return cache.Repository(
            self.addon.getAddonInfo('id'),
            xbmcmod.SimpleCache()
        )

    def _initKodiJsonrpc(self):
        return infraKodi.JsonRPC()

    def _initBetaseriesHttp(self):
        return infraBetaseries.Http(
            self.config['Betaseries']
        )
