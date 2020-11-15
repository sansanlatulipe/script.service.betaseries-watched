from resources.lib.util.di import Container
from resources.lib.infra.xbmcmod import Dialog


class Launcher:
    def __init__(self):
        self.container = Container()

    def authenticate(self):
        device = self.container.get('authentication').initialize()
        self._authenticationDialog(device)
        self.container.get('authentication').finalize(device)

    def fromScratch(self):
        if self._isMovieSynchronizationReady():
            self.container.get('movie.watch').scanAll()

    def fromLastCheckpoint(self):
        if self._isMovieSynchronizationReady():
            self.container.get('movie.watch').scanRecentlyUpdated()

    def _authenticationDialog(self, device):
        addon = self.container.get('addon')
        Dialog().notification(
            addon.getLocalizedString(20000).encode('utf-8'),
            addon.getLocalizedString(20001).format(
                device['verification_url'],
                device['user_code']
            ).encode('utf-8'),
            time=device['expires_in'] * 1000
        )

    def _isMovieSynchronizationReady(self):
        return (self.container.get('authentication').isAuthenticated()
                and self.container.settings.canSynchronizeMovies())
