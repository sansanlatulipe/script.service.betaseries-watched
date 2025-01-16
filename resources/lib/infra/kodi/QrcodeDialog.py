from tempfile import NamedTemporaryFile
import qrcode
import xbmcgui

try:
    from xbmcgui import XBFONT_CENTER_X
except ImportError:
    XBFONT_CENTER_X = 0x2


class QrcodeDialog(xbmcgui.WindowDialog):
    def __init__(self, heading: str, message: str, url: str):
        super().__init__()
        self._heading = heading
        self._message = message
        self._url = url
        self._qrcodeFile = None

    def show(self) -> None:
        self._buildQrcode()
        self._buildControls()
        super().show()

    def close(self) -> None:
        super().close()
        self._qrcodeFile.close()

    def onAction(self, action) -> None:
        self.close()

    def _buildQrcode(self) -> None:
        # pylint: disable=consider-using-with
        self._qrcodeFile = NamedTemporaryFile(suffix='.png')
        qrcodeImage = qrcode.make(self._url)
        qrcodeImage.save(self._qrcodeFile.name)

    def _buildControls(self) -> None:
        self.addControls(xbmcgui.ControlLabel(
            x=0, y=0,
            width=self.getWidth(), height=25,
            label=self._heading,
            alignment=XBFONT_CENTER_X
        ))

        self.addControl(xbmcgui.ControlLabel(
            x=0, y=50,
            width=self.getWidth(), height=50,
            label=self._message,
            alignment=XBFONT_CENTER_X
        ))

        size = min(self.getWidth(), self.getHeight()) - 200
        self.addControl(xbmcgui.ControlImage(
            x=(self.getWidth() - size) / 2, y=150,
            width=size, height=size,
            filename=self._qrcodeFile.name
        ))
