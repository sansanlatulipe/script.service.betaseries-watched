import unittest
from typing import Callable
from unittest import mock

from xbmcgui import ControlImage

from resources.lib.infra.kodi import QrcodeDialog


class QrcodeDialogShould(unittest.TestCase):
    def setUp(self) -> None:
        self.heading = 'heading'
        self.message = 'message'
        self.url = 'http://url.com'

        self.dialog = QrcodeDialog(self.heading, self.message, self.url)

    @mock.patch('tempfile._TemporaryFileWrapper')
    @mock.patch('qrcode.make')
    def test_make_qrcode_file_when_showing_dialog(self, qrCodeMaker: Callable, namedFile: Callable) -> None:
        qrCodeImage = mock.Mock()
        qrCodeMaker.return_value = qrCodeImage
        namedFile.return_value.name = 'tempfile'
        self.dialog._window.getControl = mock.Mock()

        self.dialog.show()

        qrCodeMaker.assert_called_once_with(self.url, border=1)
        qrCodeImage.save.assert_called_once_with('tempfile')

    def test_build_controls_when_showing_dialog(self) -> None:
        self.dialog._window.getControl = mock.Mock()
        self.dialog._window.addControl = mock.Mock()

        self.dialog.show()

        self.dialog._window.getControl().setLabel.assert_called_once_with(self.heading)
        self.dialog._window.getControl().setText.assert_called_once_with(self.message)
        self.assertIsInstance(self.dialog._window.addControl.call_args[0][0], ControlImage)

    @mock.patch('tempfile._TemporaryFileWrapper')
    def test_delete_temporary_file_after_showing_dialog(self, namedFile: Callable) -> None:
        tmpFile = mock.Mock()
        namedFile.return_value = tmpFile
        self.dialog._window.getControl = mock.Mock()

        self.dialog.show()

        tmpFile.close.assert_called_once()
