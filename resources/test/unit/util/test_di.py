import unittest
from unittest import mock
from resources.lib.util.di import Container


class ContainerShould(unittest.TestCase):
    def setUp(self):
        self.container = Container()

    def test_initialize_service(self):
        fakeService = object()
        self.container._initFakeService = mock.Mock(return_value=fakeService)

        service = self.container.get('fake.service')

        self.container._initFakeService.assert_called_once_with()
        self.assertEqual(fakeService, service)

    def test_return_same_service_on_successive_calls(self):
        fakeService = object()
        self.container._initFakeService = mock.Mock(return_value=fakeService)

        service1 = self.container.get('fake.service')
        service2 = self.container.get('fake.service')

        self.container._initFakeService.assert_called_once_with()
        self.assertEqual(service1, service2)

    @mock.patch('xbmcaddon.Addon')
    def test_contain_the_following_services(self, addon):
        addon().getAddonInfo.return_value = '.'

        services = [
            'addon',
            'authentication',
            'betaseries.bearer.repository',
            'betaseries.episode.repository',
            'betaseries.http',
            'betaseries.movie.repository',
            'cache.repository',
            'daemon.sync',
            'episode.sync',
            'kodi.episode.repository',
            'kodi.jsonrpc',
            'kodi.movie.repository',
            'logger',
            'movie.sync',
            'settings'
        ]
        for service in services:
            self.assertIsNotNone(self.container.get(service))
