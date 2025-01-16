from configparser import ConfigParser
from xbmcaddon import Addon


class Settings:
    def __init__(self, addon: Addon, configparser: ConfigParser):
        self.addon = addon
        self.configparser = configparser
        self.configparser.read(self.addon.getAddonInfo('path') + '/resources/data/config.ini')

    def getAddonId(self) -> str:
        return self.addon.getAddonInfo('id')

    def getBetaseriesApiKey(self) -> str:
        return self.configparser['Betaseries']

    def canSynchronize(self, kind: str) -> bool:
        return self.addon.getSetting('sync_' + kind) == 'true'

    def getBetaseriesNotifications(self) -> dict:
        return {
            'mail': lambda: self.addon.getSetting('notify_mail') == 'true',
            'twitter': lambda: self.addon.getSetting('notify_twitter') == 'true',
            'profile': lambda: self.addon.getSetting('update_profile') == 'true'
        }
