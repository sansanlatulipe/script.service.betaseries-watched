from xbmc import Monitor
from resources.lib.adapter import Settings
from resources.lib.infra.kodi import JsonRPC
from resources.lib.service import Authentication


class Deamon(Monitor):
    def __init__(self, settings: Settings, authentication: Authentication, libraries):
        super().__init__()
        self.settings = settings
        self.authentication = authentication
        self.libraries = libraries

    def run(self):
        while not self.abortRequested():
            for kind in self.libraries.keys():
                if self._isSynchronizationReady(kind):
                    self.libraries.get(kind).synchronize()
            self.waitForAbort(3600)

    def onNotification(self, sender: str, method: str, data: dict) -> None:
        if method != 'VideoLibrary.OnUpdate':
            return

        data = JsonRPC.decodeResponse(data)
        libraryKind = self._buildLibraryKindFromType(data.get('item', {}).get('type', ''))
        mediumId = data.get('item', {}).get('id')
        isNew = data.get('added')

        if self._isSynchronizationReady(libraryKind):
            if isNew:
                self.libraries.get(libraryKind).synchronizeAddedOnKodi(mediumId)
            else:
                self.libraries.get(libraryKind).synchronizeUpdatedOnKodi(mediumId)

    def _isSynchronizationReady(self, kind: str) -> bool:
        return self.authentication.isAuthenticated() \
            and self.settings.canSynchronize(kind)

    def _buildLibraryKindFromType(self, itemType: str) -> str:
        return itemType + 's'
