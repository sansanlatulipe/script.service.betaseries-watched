from configparser import ConfigParser
from unittest import mock

from behave.model import Scenario
from behave.runner import Context
from xbmcaddon import Addon

from resources.lib.adapter import CacheRepository
from resources.lib.adapter import Logger
from resources.lib.adapter import Settings
from resources.lib.infra import SimpleCache
from resources.lib.infra.betaseries import Http as BsHttp
from resources.lib.infra.kodi import JsonRPC as KodiJsonRPC
from resources.lib.util import Container


class MockContainer(Container):
    @mock.patch('xbmcaddon.Addon')
    def _initAddon(self, addonMock: Addon) -> Addon:
        addon = addonMock()

        addon.getAddonInfo.side_effect = lambda *args, **kwargs: {
            'id': 'addon.name',
            'name': 'Addon name',
            'path': '.'
        }.get(args[0])
        addon.getSetting.side_effect = lambda *args, **kwargs: {
            'sync_movies': 'true',
            'sync_episodes': 'true',
            'notify_mail': 'false',
            'notify_twitter': 'false',
            'update_profile': 'false'
        }.get(args[0])

        return addon

    @mock.patch('resources.lib.infra.betaseries.Http')
    def _initBetaseriesHttp(self, httpMock: BsHttp) -> BsHttp:
        return httpMock()

    @mock.patch('configparser.ConfigParser')
    def _initCacheRepository(self, cacheMock: SimpleCache) -> CacheRepository:
        cache = cacheMock()
        cache.get.side_effect = lambda key: {
            'addon.name.betaseries.token': 'bearer',
            'addon.name.betaseries.movie.endpoint': 1,
            'addon.name.betaseries.episode.endpoint': 2,
        }.get(key)

        return CacheRepository(
            cache,
            self.get('settings').getAddonId()
        )

    @mock.patch('resources.lib.infra.kodi.JsonRPC')
    def _initKodiJsonrpc(self, jsonMock: KodiJsonRPC) -> KodiJsonRPC:
        return jsonMock()

    @mock.patch('resources.lib.adapter.Logger')
    def _initLogger(self, loggerMock: Logger) -> Logger:
        return loggerMock()

    @mock.patch('configparser.ConfigParser')
    def _initSettings(self, configMock: ConfigParser) -> Settings:
        return Settings(
            self.get('addon'),
            configMock()
        )


def before_scenario(context: Context, scenario: Scenario) -> None:
    context.dependencyInjector = MockContainer()
