from resources.lib.util.di import Container
from resources.lib.infra.xbmcmod import Dialog


class Launcher:
    def __init__(self):
        self.container = Container()

    def authenticate(self):
        device = self.container.get('authentication').initialize()
        self._dialogAuthentication(device)
        self.container.get('authentication').finalize(device)

    def synchronize(self):
        self.container.get('daemon.sync').run()

    def _dialogAuthentication(self, device):
        addon = self.container.get('addon')
        Dialog().ok(
            addon.getLocalizedString(20000).encode('utf-8'),
            addon.getLocalizedString(20001).format(
                device['verification_url'],
                device['user_code']
            ).encode('utf-8')
        )
