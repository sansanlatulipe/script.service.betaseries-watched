import unittest
from unittest import mock
from resources.lib.infra.kodi import JsonRPC


class JsonRPCShould(unittest.TestCase):
    @mock.patch('xbmc.executeJSONRPC')
    def test_execute_jsonrpc_without_optional_arguments(self, executeJSONRPC):
        executeJSONRPC.return_value = '{}'

        JsonRPC.call('method')

        executeJSONRPC.assert_called_once_with('{"jsonrpc": "2.0", "id": 1, "method": "method", "params": {}}')
