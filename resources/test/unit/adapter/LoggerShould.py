import unittest
from typing import Callable
from unittest import mock

import xbmc
import xbmcgui
from xbmcaddon import Addon

from resources.lib.adapter import Logger


class LoggerShould(unittest.TestCase):
    @mock.patch('xbmcgui.DialogProgressBG')
    @mock.patch('xbmcgui.Dialog')
    @mock.patch('xbmcaddon.Addon')
    def setUp(
        self,
        addon: Addon,
        dialogBuilder: xbmcgui.Dialog,
        dialogProgressBuilder: xbmcgui.DialogProgressBG
    ) -> None:
        self.addon = addon()
        self.dialogBuilder = dialogBuilder
        self.dialogProgressBuilder = dialogProgressBuilder

        self.logger = Logger(self.addon, self.dialogBuilder, self.dialogProgressBuilder)

    @mock.patch('xbmc.log')
    def test_log_info_message_with_addon_name(self, log: Callable) -> None:
        self.addon.getAddonInfo.return_value = 'addon.name'

        self.logger.info('test message')

        log.assert_called_once_with('addon.name: test message', xbmc.LOGINFO)

    @mock.patch('xbmc.log')
    def test_log_error_message_with_addon_name(self, log: Callable) -> None:
        self.addon.getAddonInfo.return_value = 'addon.name'

        self.logger.error('test message')

        log.assert_called_once_with('addon.name: test message', xbmc.LOGERROR)

    def test_log_info_message_when_yelling_info(self) -> None:
        self.logger.info = mock.MagicMock()

        self.logger.yellInfo('test message')

        self.logger.info.assert_called_once_with('test message')

    def test_open_info_notification_with_log_message_when_yelling_info(self) -> None:
        self.addon.getAddonInfo.return_value = 'Addon name'

        self.logger.yellInfo('test message')

        self.dialogBuilder().notification.assert_called_once_with(
            'Addon name',
            'test message',
            icon=xbmcgui.NOTIFICATION_INFO,
            sound=False
        )

    def test_open_info_notification_with_localized_message_when_yelling_info(self) -> None:
        self.addon.getAddonInfo.return_value = 'Addon name'
        self.addon.getLocalizedString.return_value = 'localized message'

        self.logger.yellInfo('test message', 1234)

        self.dialogBuilder().notification.assert_called_once_with(
            'Addon name',
            'localized message',
            icon=xbmcgui.NOTIFICATION_INFO,
            sound=False
        )

    def test_log_error_message_when_yelling_error(self) -> None:
        self.logger.error = mock.MagicMock()

        self.logger.yellError('test message')

        self.logger.error.assert_called_once_with('test message')

    def test_open_error_notification_with_log_message_when_yelling_error(self) -> None:
        self.addon.getAddonInfo.return_value = 'Addon name'

        self.logger.yellError('test message')

        self.dialogBuilder().notification.assert_called_once_with(
            'Addon name',
            'test message',
            icon=xbmcgui.NOTIFICATION_ERROR,
            sound=True
        )

    def test_open_error_notification_with_localized_message_when_yelling_error(self) -> None:
        self.addon.getAddonInfo.return_value = 'Addon name'
        self.addon.getLocalizedString.return_value = 'localized message'

        self.logger.yellError('test message', 1234)

        self.dialogBuilder().notification.assert_called_once_with(
            'Addon name',
            'localized message',
            icon=xbmcgui.NOTIFICATION_ERROR,
            sound=True
        )

    def test_log_info_message_when_yelling_progress(self) -> None:
        self.logger.info = mock.MagicMock()

        self.logger.yellProgress(0, 'test message')

        self.logger.info.assert_called_once_with('test message (0%)')

    def test_open_progress_dialog_when_yelling_progress(self) -> None:
        self.addon.getAddonInfo.return_value = 'Addon name'

        self.logger.yellProgress(0, 'test message')

        self.dialogProgressBuilder().create.assert_called_once_with('Addon name')

    def test_update_progress_log_message_when_yelling_new_progress(self) -> None:
        self.logger.yellProgress(5, 'test message')

        self.dialogProgressBuilder().update.assert_called_once_with(
            percent=5,
            message='test message'
        )

    def test_update_progress_localized_message_when_yelling_new_progress(self) -> None:
        self.addon.getLocalizedString.return_value = 'localized message'

        self.logger.yellProgress(5, 'test message', 1234)

        self.dialogProgressBuilder().update.assert_called_once_with(
            percent=5,
            message='localized message'
        )

    def test_close_existing_progress_dialog_when_yelling_new_progress(self) -> None:
        mockProgress = mock.MagicMock()

        self.addon.getAddonInfo.return_value = 'Addon name'
        self.dialogProgressBuilder.return_value = mockProgress

        self.logger.yellProgress(0, 'test message')
        self.logger.yellProgress(0, 'test message')

        mockProgress.close.assert_called_once_with()
