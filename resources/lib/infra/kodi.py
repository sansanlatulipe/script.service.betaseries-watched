import json
from resources.lib.infra import xbmcmod


class JsonRPC:
    def call(self, method, data=None, fields=None, limit=None):
        params = data.copy() if isinstance(data, dict) else {}
        if fields:
            params['properties'] = fields
        if limit:
            params['limits'] = {'start': 0, 'end': limit}

        request = json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params
        })

        return json.loads(
            xbmcmod.executeJSONRPC(request)
        )
