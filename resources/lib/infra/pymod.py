# pylint: disable=unused-import

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser as BaseParser

    class ConfigParser(BaseParser):
        def __getitem__(self, section):
            config = {}
            for option in self.items(section):
                config[option[0]] = option[1]
            return config

try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection  # noqa: F401

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode  # noqa: F401
