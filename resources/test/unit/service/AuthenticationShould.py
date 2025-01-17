import unittest
from unittest import mock

from resources.lib.adapter import Logger
from resources.lib.adapter.betaseries import BearerRepository
from resources.lib.service import Authentication


class AuthenticationShould(unittest.TestCase):
    @mock.patch('resources.lib.adapter.betaseries.BearerRepository')
    @mock.patch('resources.lib.adapter.Logger')
    def setUp(self, logger: Logger, bearerRepo: BearerRepository) -> None:
        self.logger = logger
        self.bearerRepo = bearerRepo
        self.authentication = Authentication(self.logger, self.bearerRepo)

    def test_be_authenticated_when_bearer_exists(self) -> None:
        self.bearerRepo.isActive = mock.Mock(return_value=True)

        authenticated = self.authentication.isAuthenticated()

        self.assertTrue(authenticated)

    def test_not_be_authenticated_when_bearer_does_not_exist(self) -> None:
        self.bearerRepo.isActive = mock.Mock(return_value=False)

        authenticated = self.authentication.isAuthenticated()

        self.assertFalse(authenticated)

    def test_notify_user_when_bearer_has_not_been_initialized(self) -> None:
        self.bearerRepo.isActive = mock.Mock(return_value=None)

        authenticated = self.authentication.isAuthenticated()

        self.logger.yellError.assert_called_once_with('No BetaSeries authentication', 20002)
        self.bearerRepo.reset.assert_called_once_with()
        self.assertFalse(authenticated)

    def test_create_device_token_when_authentication_is_initialized(self) -> None:
        fakeDevice = {'token': 'random_device_identifier'}
        self.bearerRepo.createDeviceToken = mock.Mock(return_value=fakeDevice)

        device = self.authentication.initialize()

        self.bearerRepo.createDeviceToken.assert_called_once_with()
        self.assertEqual(fakeDevice, device)

    def test_create_bearer_when_authentication_is_finalized_from_device_token(self) -> None:
        fakeDevice = {'token': 'random_device_identifier'}
        fakeBearer = 'random_bearer+identifier'
        self.bearerRepo.createFromDevice = mock.Mock(return_value=fakeBearer)

        bearer = self.authentication.finalize(fakeDevice)

        self.bearerRepo.createFromDevice.assert_called_once_with(fakeDevice)
        self.assertEqual(bearer, fakeBearer)
