import json
from typing import List

import xbmc


class JsonRPC:
    @staticmethod
    def call(
        method: str,
        data: dict = None,
        fields: List[str] = None,
        limit: int = None
    ) -> dict:
        request = JsonRPC.encodeRequest(method, data, fields, limit)
        response = xbmc.executeJSONRPC(request)
        return JsonRPC.decodeResponse(response)

    @staticmethod
    def encodeRequest(
        method: str,
        data: dict = None,
        fields: List[str] = None,
        limit: int = None
    ) -> str:
        params = data.copy() if isinstance(data, dict) else {}
        if fields:
            params['properties'] = fields
        if limit is not None:
            params['limits'] = {'start': 0, 'end': limit}

        return json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params
        })

    @staticmethod
    def decodeResponse(response: str) -> dict:
        response = json.loads(response)
        if not isinstance(response, dict):
            response = {}
        if response.get('error'):
            raise IOError(response.get('error'))
        return response
