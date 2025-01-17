from unittest import mock

from behave.model import Scenario
from behave.runner import Context
from xbmcaddon import Addon

from resources.lib.adapter import CacheRepository
from resources.lib.adapter import Logger
from resources.lib.adapter.betaseries import BearerRepository
from resources.lib.adapter.betaseries import EpisodeRepository as BsEpisodeRepository
from resources.lib.adapter.betaseries import MovieRepository as BsMovieRepository
from resources.lib.adapter.kodi import EpisodeRepository as KodiEpisodeRepository
from resources.lib.adapter.kodi import MovieRepository as KodiMovieRepository
from resources.lib.util import Container


class MockContainer(Container):
    @mock.patch('xbmcaddon.Addon')
    def _initAddon(self, addon: Addon) -> Addon:
        addon().getAddonInfo.side_effect = lambda *args, **kwargs: {
            'id': 'addon.name',
            'name': 'Addon name',
            'path': '.'
        }.get(args[0])
        addon().getSetting.side_effect = lambda *args, **kwargs: {
            'sync_movies': 'true',
            'sync_episodes': 'true',
            'notify_mail': 'false',
            'notify_twitter': 'false',
            'update_profile': 'false'
        }.get(args[0])

        return addon()

    @mock.patch('resources.lib.adapter.betaseries.BearerRepository')
    def _initBetaseriesBearerRepository(self, repo: BearerRepository) -> BearerRepository:
        return repo

    @mock.patch('resources.lib.adapter.betaseries.EpisodeRepository')
    def _initBetaseriesEpisodeRepository(self, repo: BsEpisodeRepository) -> BsEpisodeRepository:
        return repo

    @mock.patch('resources.lib.adapter.betaseries.MovieRepository')
    def _initBetaseriesMovieRepository(self, repo: BsMovieRepository) -> BsMovieRepository:
        return repo

    @mock.patch('resources.lib.adapter.CacheRepository')
    def _initCacheRepository(self, repo: CacheRepository) -> CacheRepository:
        return repo

    @mock.patch('resources.lib.adapter.kodi.EpisodeRepository')
    def _initKodiEpisodeRepository(self, repo: KodiEpisodeRepository) -> KodiEpisodeRepository:
        return repo

    @mock.patch('resources.lib.adapter.kodi.MovieRepository')
    def _initKodiMovieRepository(self, repo: KodiMovieRepository) -> KodiMovieRepository:
        return repo

    @mock.patch('resources.lib.adapter.Logger')
    def _initLogger(self, logger: Logger) -> Logger:
        return logger


def before_scenario(context: Context, scenario: Scenario) -> None:
    context.dependencyInjector = MockContainer()
