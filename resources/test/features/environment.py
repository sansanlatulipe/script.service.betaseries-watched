from unittest import mock
from resources.lib.util import Container


class MockContainer(Container):
    @mock.patch('xbmcaddon.Addon')
    def _initAddon(self, addon):
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
    def _initBetaseriesBearerRepository(self, repo):
        return repo

    @mock.patch('resources.lib.adapter.betaseries.EpisodeRepository')
    def _initBetaseriesEpisodeRepository(self, repo):
        return repo

    @mock.patch('resources.lib.adapter.betaseries.MovieRepository')
    def _initBetaseriesMovieRepository(self, repo):
        return repo

    @mock.patch('resources.lib.adapter.CacheRepository')
    def _initCacheRepository(self, repo):
        return repo

    @mock.patch('resources.lib.adapter.kodi.EpisodeRepository')
    def _initKodiEpisodeRepository(self, repo):
        return repo

    @mock.patch('resources.lib.adapter.kodi.MovieRepository')
    def _initKodiMovieRepository(self, repo):
        return repo

    @mock.patch('resources.lib.adapter.Logger')
    def _initLogger(self, logger):
        return logger


def before_scenario(context, scenario):
    context.dependencyInjector = MockContainer()
