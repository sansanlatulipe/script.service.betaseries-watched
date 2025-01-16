import xbmc
import xbmcgui
from xbmcaddon import Addon


class Logger:
    def __init__(
        self,
        addon: Addon,
        dialogBuilder: xbmcgui.Dialog,
        dialogProgressBuilder: xbmcgui.DialogProgressBG
    ) -> None:
        self.addon = addon
        self.dialogBuilder = dialogBuilder
        self.dialogProgressBuilder = dialogProgressBuilder

        self.dialogProgress = None

    def info(self, msg: str) -> None:
        self._log(msg, xbmc.LOGINFO)

    def error(self, msg: str) -> None:
        self._log(msg, xbmc.LOGERROR)

    def yellInfo(self, msg: str, localizedLabel: int = None) -> None:
        self.info(msg)

        self._closeExistingProgress()
        self.dialogBuilder().notification(
            self.addon.getAddonInfo('name'),
            self._buildLocalizedMessage(localizedLabel, msg),
            icon=xbmcgui.NOTIFICATION_INFO,
            sound=False
        )

    def yellProgress(self, percent: int, msg: str, localizedLabel: int = None) -> None:
        self.info(f'{msg} ({percent}%)')

        if not self.dialogProgress or percent == 0:
            self._closeExistingProgress()
            self.dialogProgress = self.dialogProgressBuilder()
            self.dialogProgress.create(self.addon.getAddonInfo('name'))

        self.dialogProgress.update(
            percent=percent,
            message=self._buildLocalizedMessage(localizedLabel, msg)
        )

    def yellError(self, msg: str, localizedLabel: int = None) -> None:
        self.error(msg)

        self._closeExistingProgress()
        self.dialogBuilder().notification(
            self.addon.getAddonInfo('name'),
            self._buildLocalizedMessage(localizedLabel, msg),
            icon=xbmcgui.NOTIFICATION_ERROR,
            sound=True
        )

    def _buildLocalizedMessage(self, localizedLabel: int, defaultMsg: str) -> str:
        return self.addon.getLocalizedString(localizedLabel) if localizedLabel else defaultMsg

    def _closeExistingProgress(self) -> None:
        if self.dialogProgress:
            self.dialogProgress.close()
            self.dialogProgress = None

    def _log(self, msg: str, loglvl: int) -> None:
        xbmc.log('{}: {}'.format(self.addon.getAddonInfo('id'), msg), loglvl)
