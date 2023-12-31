import json
from resources.lib.infra import xbmcmod


class JsonRPC:
    @staticmethod
    def call(method, data=None, fields=None, limit=None):
        request = JsonRPC.encodeRequest(method, data, fields, limit)
        response = xbmcmod.executeJSONRPC(request)
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
