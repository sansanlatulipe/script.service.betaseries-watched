import unittest
from unittest import mock
from resources.lib.service import Deamon


class DeamonShould(unittest.TestCase):
    @mock.patch('resources.lib.service.WatchSynchro')
    @mock.patch('resources.lib.service.Authentication')
    @mock.patch('resources.lib.adapter.Settings')
    def setUp(self, settings, authentication, library):
        self.settings = settings()
        self.authentication = authentication()
        self.library = library()
        libraries = {'movies': self.library, 'episodes': self.library}
        self.daemon = Deamon(self.settings, self.authentication, libraries)

        self.daemon.abortRequested = mock.Mock(side_effect=[False, True])

    def test_run_while_no_abort_is_requested(self):
        self.daemon.waitForAbort = mock.Mock()

        self.daemon.run()

        self.daemon.waitForAbort.assert_called_once_with(3600)
        self.assertEqual(2, self.daemon.abortRequested.call_count)

    def test_synchronize_every_library_while_running(self):
        self.daemon.run()

        self.assertEqual(2, self.library.synchronize.call_count)

    def test_check_authentication_is_ready_before_synchronizing(self):
        self.authentication.isAuthenticated = mock.Mock(return_value=False)

        self.daemon.run()

        self.assertEqual(2, self.authentication.isAuthenticated.call_count)
        self.library.synchronize.assert_not_called()

    def test_check_can_synchronize_media_kind_before_running_it(self):
        self.settings.canSynchronize = mock.Mock(side_effect=[False, True])

        self.daemon.run()

        self.settings.canSynchronize.assert_has_calls([
            mock.call('movies'),
            mock.call('episodes')
        ])
        self.library.synchronize.assert_called_once()

    def test_ignore_all_notifications_but_video_updates(self):
        self.daemon.onNotification('me', 'Fake.Event', '{"item": {"type": "movie"}}')

        self.library.synchronizeUpdatedOnKodi.assert_not_called()

    def test_ignore_all_notifications_not_regarding_a_managed_library(self):
        self.settings.canSynchronize = mock.Mock(return_value=False)

        self.daemon.onNotification('me', 'VideoLibrary.OnUpdate', '{"item": {"type": "music"}}')

        self.settings.canSynchronize.assert_called_once_with('musics')
        self.library.synchronizeUpdatedOnKodi.assert_not_called()

    def test_synchronize_kodi_medium_with_betaseries_when_added_to_library(self):
        self.daemon.onNotification('me', 'VideoLibrary.OnUpdate', """{
            "added": true,
            "item": {
                "id": "kodi-1",
                "type": "movie"
            }
        }""")

        self.library.synchronizeAddedOnKodi.assert_called_once_with('kodi-1')

    def test_synchronize_kodi_medium_with_betaseries_when_updated_to_library(self):
        self.daemon.onNotification('me', 'VideoLibrary.OnUpdate', """{
            "added": false,
            "item": {
                "id": "kodi-1",
                "type": "movie"
            }
        }""")

        self.library.synchronizeUpdatedOnKodi.assert_called_once_with('kodi-1')
