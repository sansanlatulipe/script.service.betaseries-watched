from resources.lib.util.di import Container
from resources.lib.infra.xbmcmod import Dialog


def fromScratch():
    container = Container()
    container.get('authentication').authenticate()
    container.get('movie.watch').scanAll()


def fromLastCheckpoint():
    container = Container()
    container.get('authentication').authenticate()
    container.get('movie.watch').scanRecentlyUpdated()


def authenticate():
    container = Container()
    device = container.get('authentication').initialize()
    _authenticationDialog(container.addon, device)
    container.get('authentication').finalize(device)


def _authenticationDialog(addon, device):
    Dialog().textviewer(
        addon.getLocalizedString(20000).encode('utf-8'),
        addon.getLocalizedString(20001).format(
            device['verification_url'],
            device['user_code']
        ).encode('utf-8')
    )
