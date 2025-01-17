import json
import unittest
from typing import Callable
from unittest import mock

from resources.lib.infra.kodi import JsonRPC


class JsonRPCShould(unittest.TestCase):
    @mock.patch('xbmc.executeJSONRPC')
    def test_execute_jsonrpc_without_optional_arguments(self, executeJSONRPC: Callable) -> None:
        executeJSONRPC.return_value = '{}'

        JsonRPC.call('method')

        executeJSONRPC.assert_called_once_with(json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'method',
            'params': {}
        }))

    @mock.patch('xbmc.executeJSONRPC')
    def test_execute_jsonrpc_with_data(self, executeJSONRPC: Callable) -> None:
        executeJSONRPC.return_value = '{}'

        JsonRPC.call('method', data={'key': 'value'})

        executeJSONRPC.assert_called_once_with(json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'method',
            'params': {
                'key': 'value'
            }
        }))

    @mock.patch('xbmc.executeJSONRPC')
    def test_execute_jsonrpc_with_fields(self, executeJSONRPC: Callable) -> None:
        executeJSONRPC.return_value = '{}'

        JsonRPC.call('method', fields=['field1'])

        executeJSONRPC.assert_called_once_with(json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'method',
            'params': {
                'properties': ['field1']
            }
        }))

    @mock.patch('xbmc.executeJSONRPC')
    def test_execute_jsonrpc_with_limit(self, executeJSONRPC: Callable) -> None:
        executeJSONRPC.return_value = '{}'

        JsonRPC.call('method', limit=10)

        executeJSONRPC.assert_called_once_with(json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'method',
            'params': {
                'limits': {'start': 0, 'end': 10}
            }
        }))

    @mock.patch('xbmc.executeJSONRPC')
    def test_execute_jsonrpc_with_data_fields_and_limit(self, executeJSONRPC: Callable) -> None:
        executeJSONRPC.return_value = '{}'

        JsonRPC.call('method', data={'key': 'value'}, fields=['fields'], limit=10)

        executeJSONRPC.assert_called_once_with(json.dumps({
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'method',
            'params': {
                'key': 'value',
                'properties': ['fields'],
                'limits': {'start': 0, 'end': 10}
            }
        }))

    @mock.patch('xbmc.executeJSONRPC')
    def test_build_dict_from_jsonrpc_response(self, executeJSONRPC: Callable) -> None:
        expectedResponse = {'key': 'value'}
        executeJSONRPC.return_value = json.dumps(expectedResponse)

        actualResponse = JsonRPC.call('method')

        self.assertEqual(expectedResponse, actualResponse)

    @mock.patch('xbmc.executeJSONRPC')
    def test_raise_exception_when_jsonrpc_response_contains_error(self, executeJSONRPC: Callable) -> None:
        executeJSONRPC.return_value = json.dumps({'error': 'message'})

        with self.assertRaises(IOError):
            JsonRPC.call('method')
