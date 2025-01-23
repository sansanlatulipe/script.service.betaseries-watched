import unittest
from typing import Callable
from unittest import mock

from xbmcgui import ControlImage
from xbmcgui import ControlLabel

from resources.lib.infra.kodi import QrcodeDialog


class QrcodeDialogShould(unittest.TestCase):
    def setUp(self) -> None:
        self.heading = 'heading'
        self.message = 'message'
        self.url = 'http://url.com'

        self.dialog = QrcodeDialog(self.heading, self.message, self.url)

    @mock.patch('qrcode.make')
    def test_make_qrcode_file_when_showing_dialog(self, qrCodeMaker: Callable) -> None:
        qrCodeImage = mock.Mock()
        qrCodeMaker.return_value = qrCodeImage

        self.dialog.show()

        qrCodeMaker.assert_called_once_with(self.url)

    def test_add_controls_when_showing_dialog(self) -> None:
        self.dialog.addControl = mock.Mock()

        self.dialog.show()

        self.assertEqual(3, self.dialog.addControl.call_count)
        self.assertIsInstance(self.dialog.addControl.call_args_list[0].args[0], ControlLabel)
        self.assertIsInstance(self.dialog.addControl.call_args_list[1].args[0], ControlLabel)
        self.assertIsInstance(self.dialog.addControl.call_args_list[2].args[0], ControlImage)

    def test_delete_temporary_file_when_closing_dialog(self) -> None:
        self.dialog._qrcodeFile = mock.Mock()

        self.dialog.close()

        self.dialog._qrcodeFile.close.assert_called_once()
