import json
from http.client import HTTPSConnection
from urllib.parse import urlencode


class Http:
    def __init__(self, config: dict) -> None:
        self.version = config['version']
        self.clientId = config['client_id']
        self.clientSecret = config['client_secret']
        self.bearer = None
        self.http = HTTPSConnection(config['url'])

    def get(self, uri: str, data: dict = None) -> dict:
        if data:
            uri += '?' + urlencode(data)
        return self._call('GET', uri)

    def post(self, uri: str, data: dict = None) -> dict:
        if isinstance(data, dict):
            data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
        else:
            headers = None
        return self._call('POST', uri, data, headers)

    def delete(self, uri: str, data: dict = None) -> dict:
        if data:
            uri += '?' + urlencode(data)
        return self._call('DELETE', uri)

    def _call(self, method: str, uri: str, body: str = None, headers: dict = None) -> dict:
        self.http.request(
            method,
            uri,
            body,
            self._initHeaders(headers)
        )
        return self._decodeResponse(
            self.http.getresponse().read().decode()
        )

    def _initHeaders(self, headers: dict) -> dict:
        headers = headers or {}
        headers.update({
            'Accept': 'application/json',
            'X-BetaSeries-Version': self.version,
            'X-BetaSeries-Key': self.clientId
        })
        if self.bearer:
            headers['Authorization'] = 'Bearer ' + self.bearer
        return headers

    def _decodeResponse(self, response: str) -> dict:
        response = json.loads(response)
        if response.get('errors'):
            raise IOError(response.get('errors'))
        return response
