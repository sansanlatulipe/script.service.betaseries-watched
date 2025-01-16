from typing import Any


try:
    from simplecache import SimpleCache
except ImportError:
    class SimpleCache:
        def __init__(self) -> None:
            self.cached = {}

        def get(self, key: str) -> Any:
            return self.cached.get(key)

        def set(self, key: str, value: Any) -> None:
            self.cached[key] = value
