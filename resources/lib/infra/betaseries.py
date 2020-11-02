import json
from resources.lib.infra.pymod import HTTPConnection


class Http:
    def __init__(self, config):
        self.version = config['version']
        self.clientId = config['client_id']
        self.clientSecret = config['client_secret']
        self.bearer = None
        self.http = HTTPConnection(config['url'])

    def call(self, method, uri, data=None):
        self.http.request(
            method,
            uri,
            self._encodeData(data),
            self._initHeaders(data)
        )
        return self._decodeResponse(
            self.http.getresponse().read().decode()
        )

    def _initHeaders(self, data):
        headers = {
            'Accept': 'application/json',
            'X-BetaSeries-Version': self.version,
            'X-BetaSeries-Key': self.clientId
        }
        if self.bearer is not None:
            headers['Authorization'] = 'Bearer ' + self.bearer
        if isinstance(data, dict):
            headers['Content-Type'] = 'application/json'
        return headers

    def _encodeData(self, data):
        if isinstance(data, dict):
            return json.dumps(data)
        return data

    def _decodeResponse(self, response):
        response = json.loads(response)
        if response.get('errors'):
            raise IOError(response['errors'])
        return response
