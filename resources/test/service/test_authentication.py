import unittest
from resources.test.mock import patch
from resources.test.mock import MagicMock
from resources.lib.service.authentication import Authentication


class AuthenticationShould(unittest.TestCase):
    @patch('resources.lib.appli.betaseries.BearerRepository')
    def setUp(self, bearerRepo):
        self.bearerRepo = bearerRepo
        self.authentication = Authentication(bearerRepo)

    def test_be_authenticated_when_bearer_exists(self):
        self.bearerRepo.exists = MagicMock(return_value=True)

        authenticated = self.authentication.isAuthenticated()

        self.bearerRepo.exists.assert_called_once_with()
        self.assertTrue(authenticated)

    def test_create_device_token_when_authentication_is_initialized(self):
        fakeDevice = {'token': 'random_device_identifier'}
        self.bearerRepo.createDeviceToken = MagicMock(return_value=fakeDevice)

        device = self.authentication.initialize()

        self.bearerRepo.createDeviceToken.assert_called_once_with()
        self.assertEqual(device, fakeDevice)

    def test_create_bearer_when_authentication_is_finalized_from_device_token(self):
        fakeDevice = {'token': 'random_device_identifier'}
        fakeBearer = 'random_bearer+identifier'
        self.bearerRepo.createFromDevice = MagicMock(return_value=fakeBearer)

        bearer = self.authentication.finalize(fakeDevice)

        self.bearerRepo.createFromDevice.assert_called_once_with(fakeDevice)
        self.assertEqual(bearer, fakeBearer)
