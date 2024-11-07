# pylint: disable=unused-import
# flake8: noqa

try:
    from simplecache import SimpleCache
except ImportError:
    class SimpleCache:
        def __init__(self):
            self.cached = {}

        def get(self, key):
            return self.cached.get(key)

        def set(self, key, value):
            self.cached[key] = value
