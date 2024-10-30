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
    import os


    LOGDEBUG = 'DEBUG'
    LOGINFO = 'INFO'
    LOGWARNING = 'WARNING'
    LOGERROR = 'ERROR'
    NOTIFICATION_INFO = 'INFO'
    NOTIFICATION_WARNING = 'WARNING'
    NOTIFICATION_ERROR = 'ERROR'

    def log(msg, level):
        print(level, msg)


    def executeJSONRPC(jsonrpccommand):
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
            if key == 'name':
                return 'Fake add-on'
            if key == 'path':
                path = os.path.abspath(__file__)
                for _ in range(4):
                    path = os.path.dirname(path)
                return path
            return None

        def getSetting(self, key):
            return self.settings.get(key)

        def getLocalizedString(self, key):
            return 'Message {}'.format(key)


    class Dialog:
        def ok(self, heading, message):
            print('{} > {}'.format(heading, message))

        def notification(self, heading, message, icon=NOTIFICATION_INFO, time=5000, sound=True):
            print('[{}] {} > {}'.format(icon, heading, message))


    class DialogProgressBG:
        def create(self, heading, message=None):
            print('{} > {}'.format(heading, message))

        def update(self, percent, heading=None, message=None):
            print('{} > {} ({}%)'.format(heading, message, percent))

        def close(self):
            pass


    class SimpleCache:
        def __init__(self):
            self.cached = {}

        def get(self, key):
            return self.cached.get(key)

        def set(self, key, value):
            self.cached[key] = value
