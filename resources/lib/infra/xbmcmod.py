# pylint: disable=unused-import
# flake8: noqa

try:
    from xbmc import log, LOGDEBUG, LOGINFO, LOGWARNING, LOGERROR
    from xbmc import executeJSONRPC
    from xbmc import Monitor
    from xbmcaddon import Addon
    from xbmcgui import Dialog, NOTIFICATION_INFO, NOTIFICATION_WARNING, NOTIFICATION_ERROR
    from xbmcgui import DialogProgressBG
    from simplecache import SimpleCache
except ImportError:
    LOGDEBUG = 'DEBUG'
    LOGINFO = 'INFO'
    LOGWARNING = 'WARNING'
    LOGERROR = 'ERROR'
    NOTIFICATION_INFO = 'INFO'
    NOTIFICATION_WARNING = 'WARNING'
    NOTIFICATION_ERROR = 'ERROR'

    def log(msg, lvl):
        print(lvl, msg)


    def executeJSONRPC(query):
        return '{"result":{"movies":[],"moviedetails":{}}}'


    class Monitor:
        def __init__(self):
            self.requests = 0

        def waitForAbort(self, timeout=0):
            pass

        def abortRequested(self):
            self.requests += 1
            return self.requests > 1


    class Addon:
        def __init__(self):
            self.settings = {
                'sync_movies': 'true',
                'sync_tvshows': 'false',
                'notify_mail': 'false',
                'notify_twitter': 'false',
                'update_profile': 'false'
            }

        def getAddonInfo(self, key):
            if key == 'id':
                return 'addon.fake'
            if key == 'path':
                return '.'
            return None

        def getSetting(self, key):
            return self.settings.get(key)

        def getLocalizedString(self, labelId):
            return 'Message {}'.format(labelId)


    class Dialog:
        def ok(self, heading, text):
            print('{} > {}'.format(heading, text))

        def notification(self, heading, text, icon=NOTIFICATION_INFO, time=5000, sound=True):
            print('[{}] {} > {}'.format(icon, heading, text))


    class DialogProgressBG:
        def create(self, heading, msg):
            print('{} > {}'.format(heading, msg))

        def update(self, percent, heading=None, msg=None):
            print('{} > {} ({}%)'.format(heading, msg, percent))

        def close(self):
            pass


    class SimpleCache:
        def __init__(self):
            self.cached = {}

        def get(self, key):
            return self.cached.get(key)

        def set(self, key, value):
            self.cached[key] = value
