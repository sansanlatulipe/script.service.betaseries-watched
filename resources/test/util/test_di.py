import unittest
from resources.lib.util.di import Container
from resources.lib.infra.kodi import JsonRPC


class ContainerShould(unittest.TestCase):
    def setUp(self):
        self.container = Container()

    def test_initialize_service(self):
        service = self.container.get('kodi.jsonrpc')
        self.assertIsInstance(service, JsonRPC)

    def test_return_same_service_on_successive_calls(self):
        service1 = self.container.get('kodi.jsonrpc')
        service2 = self.container.get('kodi.jsonrpc')
        self.assertEqual(service1, service2)

    def test_contain_the_following_services(self):
        services = [
            'authentication',
            'betaseries.bearer.repository',
            'betaseries.http',
            'betaseries.movie.repository',
            'cache.repository',
            'kodi.jsonrpc',
            'kodi.movie.repository',
            'movie.watch'
        ]
        for service in services:
            self.assertIsNotNone(self.container.get(service))
