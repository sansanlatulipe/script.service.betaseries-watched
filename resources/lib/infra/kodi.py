import json
from tempfile import NamedTemporaryFile
import qrcode
import xbmc
import xbmcgui
from resources.lib.infra import xbmcmod


class JsonRPC:
    @staticmethod
    def call(method, data=None, fields=None, limit=None):
        request = JsonRPC.encodeRequest(method, data, fields, limit)
        response = xbmc.executeJSONRPC(request)
        return JsonRPC.decodeResponse(response)

    @staticmethod
    def encodeRequest(method, data, fields, limit):
        params = data.copy() if isinstance(data, dict) else {}
        if fields:
            params['properties'] = fields
        if limit:
            params['limits'] = {'start': 0, 'end': limit}

        return json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params
        })

    @staticmethod
    def decodeResponse(response):
        response = json.loads(response)
        if not isinstance(response, dict):
            response = {}
        if response.get('error'):
            raise IOError(response.get('error'))
        return response


class QrcodeDialog(xbmcgui.WindowDialog):
    def __init__(self, heading, message, url):
        super().__init__()
        self._heading = heading
        self._message = message
        self._url = url
        self._qrcodeFile = None

    def show(self):
        self._buildQrcode()
        self._buildControls()
        super().show()

    def close(self):
        super().close()
        self._qrcodeFile.close()

    def onAction(self, action):
        self.close()

    def _buildQrcode(self):
        # pylint: disable=consider-using-with
        self._qrcodeFile = NamedTemporaryFile(suffix='.png')
        qrcodeImage = qrcode.make(self._url)
        qrcodeImage.save(self._qrcodeFile.name)

    def _buildControls(self):
        self.addControls(xbmcgui.ControlLabel(
            x=0, y=0,
            width=self.getWidth(), height=25,
            label=self._heading,
            alignment=xbmcmod.XBFONT_CENTER_X
        ))

        self.addControl(xbmcgui.ControlLabel(
            x=0, y=50,
            width=self.getWidth(), height=50,
            label=self._message,
            alignment=xbmcmod.XBFONT_CENTER_X
        ))

        size = min(self.getWidth(), self.getHeight()) - 200
        self.addControl(xbmcgui.ControlImage(
            x=(self.getWidth() - size) / 2, y=150,
            width=size, height=size,
            filename=self._qrcodeFile.name
        ))
