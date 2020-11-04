# pylint: disable=unused-import,ungrouped-imports
# flake8: noqa

try:
    from configparser import ConfigParser
    from http.client import HTTPConnection
    from urllib.parse import urlencode
except ImportError:
    from ConfigParser import ConfigParser as BaseParser
    from httplib import HTTPConnection
    from urllib import urlencode


    class ConfigParser(BaseParser):
        def __getitem__(self, section):
            config = {}
            for option in self.items(section):
                config[option[0]] = option[1]
            return config
