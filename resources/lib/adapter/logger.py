from resources.lib.infra import xbmcmod


class Logger:
    def __init__(self, addon, dialogBuilder, dialogProgressBuilder):
        self.addon = addon
        self.dialogBuilder = dialogBuilder
        self.dialogProgressBuilder = dialogProgressBuilder

        self.dialogProgress = None

    def info(self, msg):
        xbmcmod.log(msg, xbmcmod.LOGINFO)

    def error(self, msg):
        xbmcmod.log(msg, xbmcmod.LOGERROR)

    def yellInfo(self, msg, localizedLabel=None):
        self.info(msg)

        self._closeExistingProgress()
        self.dialogBuilder().notification(
            self.addon.getAddonInfo('name'),
            self._buildLocalizedMessage(localizedLabel, msg),
            icon=xbmcmod.NOTIFICATION_INFO,
            sound=False
        )

    def yellProgress(self, percent, msg, localizedLabel=None):
        self.info(f'{msg} ({percent}%)')

        if not self.dialogProgress or percent == 0:
            self._closeExistingProgress()
            self.dialogProgress = self.dialogProgressBuilder()
            self.dialogProgress.create(self.addon.getAddonInfo('name'))

        self.dialogProgress.update(
            percent,
            self._buildLocalizedMessage(localizedLabel, msg)
        )

    def yellError(self, msg, localizedLabel=None):
        self.error(msg)

        self._closeExistingProgress()
        self.dialogBuilder().notification(
            self.addon.getAddonInfo('name'),
            self._buildLocalizedMessage(localizedLabel, msg),
            icon=xbmcmod.NOTIFICATION_ERROR,
            sound=True
        )

    def _buildLocalizedMessage(self, localizedLabel, defaultMsg):
        return self.addon.getLocalizedString(localizedLabel) if localizedLabel else defaultMsg

    def _closeExistingProgress(self):
        if self.dialogProgress:
            self.dialogProgress.close()
            self.dialogProgress = None
