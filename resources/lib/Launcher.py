from resources.lib.infra.kodi import QrcodeDialog
from resources.lib.util import Container


class Launcher:
    def __init__(self) -> None:
        self.container = Container()

    def authenticate(self) -> None:
        device = self.container.get('authentication').initialize()
        self._dialogAuthentication(device)
        self.container.get('authentication').finalize(device)

    def synchronize(self) -> None:
        self.container.get('daemon.sync').run()

    def _dialogAuthentication(self, device: dict) -> None:
        addon = self.container.get('addon')
        dialog = QrcodeDialog(
            addon.getLocalizedString(20000).encode('utf-8'),
            addon.getLocalizedString(20001).format(
                device.get('verification_url'),
                device.get('user_code')
            ).encode('utf-8'),
            device.get('verification_url')
        )
        dialog.show()
