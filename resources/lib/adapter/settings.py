class Settings:
    def __init__(self, addon, configparser):
        self.addon = addon
        self.configparser = configparser
        print(self.addon.getAddonInfo('path') + '/resources/data/config.ini')
        self.configparser.read(self.addon.getAddonInfo('path') + '/resources/data/config.ini')

    def getAddonId(self):
        return self.addon.getAddonInfo('id')

    def getBetaseriesApiKey(self):
        return self.configparser['Betaseries']

    def canSynchronize(self, kind):
        return self.addon.getSetting('sync_' + kind) == 'true'

    def getBetaseriesNotifications(self):
        return {
            'mail': lambda: self.addon.getSetting('notify_mail') == 'true',
            'twitter': lambda: self.addon.getSetting('notify_twitter') == 'true',
            'profile': lambda: self.addon.getSetting('update_profile') == 'true'
        }
