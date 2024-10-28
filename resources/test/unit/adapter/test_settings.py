from resources.test.unit.testmod import unittest
from resources.test.unit.testmod import mock
from resources.lib.adapter import settings


class SettingsShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.xbmcmod.Addon')
    def setUp(self, addon):
        self.addon = addon
        self.configparser = mock.Mock()
        self.settings = settings.Settings(self.addon, self.configparser)

    def test_get_addon_id_from_addon_info(self):
        expectedAddonId = 'hyperion-instance'
        self.addon.getAddonInfo = mock.Mock(return_value=expectedAddonId)

        addonId = self.settings.getAddonId()

        self.addon.getAddonInfo.assert_called_once_with('id')
        self.assertEqual(expectedAddonId, addonId)

    def test_get_betaseries_api_key_from_config(self):
        expectedConfig = {
            'version': '1.0',
            'client_id': 'client',
            'client_secret': 'expected_api_key'
        }
        self.configparser.__getitem__ = mock.Mock(return_value=expectedConfig)

        config = self.settings.getBetaseriesApiKey()

        self.configparser.__getitem__.assert_called_once_with('Betaseries')
        self.assertEqual(expectedConfig, config)

    def test_get_synchronization_permission_from_addon_settings(self):
        self.addon.getSetting = mock.Mock(return_value='true')

        setting = self.settings.canSynchronize('movies')

        self.addon.getSetting.assert_called_once_with('sync_movies')
        self.assertTrue(setting)

    def test_get_betaseries_mail_notification_permission_from_addon_settings(self):
        self.addon.getSetting = mock.Mock(return_value='true')

        setting = self.settings.getBetaseriesNotifications()

        self.assertTrue(setting['mail']())
        self.addon.getSetting.assert_called_once_with('notify_mail')

    def test_get_betaseries_twitter_notification_permission_from_addon_settings(self):
        self.addon.getSetting = mock.Mock(return_value='false')

        setting = self.settings.getBetaseriesNotifications()

        self.assertFalse(setting['twitter']())
        self.addon.getSetting.assert_called_once_with('notify_twitter')

    def test_get_betaseries_profile_update_permission_from_addon_settings(self):
        self.addon.getSetting = mock.Mock(return_value='true')

        setting = self.settings.getBetaseriesNotifications()

        self.assertTrue(setting['profile']())
        self.addon.getSetting.assert_called_once_with('update_profile')
