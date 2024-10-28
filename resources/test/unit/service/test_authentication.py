from resources.test.unit.testmod import unittest
from resources.test.unit.testmod import mock
from resources.lib.service.authentication import Authentication


class AuthenticationShould(unittest.TestCase):
    @mock.patch('resources.lib.adapter.betaseries.BearerRepository')
    def setUp(self, bearerRepo):
        self.bearerRepo = bearerRepo
        self.authentication = Authentication(self.bearerRepo)

    def test_be_authenticated_when_bearer_exists(self):
        self.bearerRepo.exists = mock.Mock(return_value=True)

        authenticated = self.authentication.isAuthenticated()

        self.bearerRepo.exists.assert_called_once_with()
        self.assertTrue(authenticated)

    def test_create_device_token_when_authentication_is_initialized(self):
        fakeDevice = {'token': 'random_device_identifier'}
        self.bearerRepo.createDeviceToken = mock.Mock(return_value=fakeDevice)

        device = self.authentication.initialize()

        self.bearerRepo.createDeviceToken.assert_called_once_with()
        self.assertEqual(fakeDevice, device)

    def test_create_bearer_when_authentication_is_finalized_from_device_token(self):
        fakeDevice = {'token': 'random_device_identifier'}
        fakeBearer = 'random_bearer+identifier'
        self.bearerRepo.createFromDevice = mock.Mock(return_value=fakeBearer)

        bearer = self.authentication.finalize(fakeDevice)

        self.bearerRepo.createFromDevice.assert_called_once_with(fakeDevice)
        self.assertEqual(bearer, fakeBearer)
