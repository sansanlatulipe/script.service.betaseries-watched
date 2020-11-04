class Settings:
    def __init__(self, addon, configparser):
        self.addon = addon
        self.configparser = configparser
        self.configparser.read(self.addon.getAddonInfo('path') + '/resources/data/config.ini')

    def getAddonId(self):
        return self.addon.getAddonInfo('id')

    def getBetaseriesApiKey(self):
        return self.configparser['Betaseries']

    def canSynchronizeMovies(self):
        return self.addon.getSetting('sync_movies') == 'true'

    def canSynchronizeTvShows(self):
        return self.addon.getSetting('sync_tvshows') == 'true'

    def getBetaseriesNotifications(self):
        return {
            'notify_mail': self.addon.getSetting('notify_mail') == 'true',
            'notify_twitter': self.addon.getSetting('notify_twitter') == 'true',
            'update_profile': self.addon.getSetting('update_profile') == 'true'
        }
