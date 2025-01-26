from tempfile import NamedTemporaryFile

import qrcode
import xbmc
from xbmcgui import ControlImage
from xbmcgui import WindowXMLDialog


class QrcodeDialog:
    def __init__(self, heading: str, message: str, url: str) -> None:
        self._heading = heading
        self._message = message
        self._url = url

        self._window = WindowXMLDialog('DialogTextViewer.xml', xbmc.getSkinDir())
        self._qrcodeFile = None

    def __del__(self) -> None:
        del self._qrcodeFile
        del self._window

    def show(self) -> None:
        self._window.show()

        self._buildQrcode()
        self._buildControls()

        self._qrcodeFile.close()

    def _buildQrcode(self) -> None:
        self._qrcodeFile = NamedTemporaryFile(suffix='.png')
        qrcodeImage = qrcode.make(self._url, border=1)
        qrcodeImage.save(self._qrcodeFile.name)

    def _buildControls(self) -> None:
        self._window.getControl(1).setLabel(self._heading)

        self._window.getControl(5).setText(self._message)

        windowWidth = self._window.getWidth()
        windowHeight = self._window.getHeight()
        qrcodeSize = int(min(windowWidth, windowHeight) * 0.5)
        self._window.addControl(ControlImage(
            x=int((windowWidth - qrcodeSize) / 2), y=int(windowHeight / 3),
            width=qrcodeSize, height=qrcodeSize,
            filename=self._qrcodeFile.name
        ))
