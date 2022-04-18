import json
from http.client import HTTPConnection
from urllib.parse import urlencode


class Http:
    def __init__(self, config):
        self.version = config['version']
        self.clientId = config['client_id']
        self.clientSecret = config['client_secret']
        self.bearer = None
        self.http = HTTPConnection(config['url'])

    def get(self, uri, data=None):
        if data:
            uri += '?' + urlencode(data)
        return self._call('GET', uri)

    def post(self, uri, data=None):
        if isinstance(data, dict):
            data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
        else:
            headers = None
        return self._call('POST', uri, data, headers)

    def _call(self, method, uri, body=None, headers=None):
        self.http.request(
            method,
            uri,
            body,
            self._initHeaders(headers)
        )
        return self._decodeResponse(
            self.http.getresponse().read().decode()
        )

    def _initHeaders(self, headers):
        headers = headers or {}
        headers.update({
            'Accept': 'application/json',
            'X-BetaSeries-Version': self.version,
            'X-BetaSeries-Key': self.clientId
        })
        if self.bearer:
            headers['Authorization'] = 'Bearer ' + self.bearer
        return headers

    def _decodeResponse(self, response):
        response = json.loads(response)
        if response.get('errors'):
            raise IOError(response.get('errors'))
        return response
