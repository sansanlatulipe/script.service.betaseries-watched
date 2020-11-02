import json
from resources.lib.infra import xbmcmod


class JsonRPC:
    def call(self, method, data=None, fields=None):
        params = data.copy() if isinstance(data, dict) else {}
        if fields:
            params['properties'] = fields

        request = json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params
        })

        return json.loads(
            xbmcmod.executeJSONRPC(request)
        )
