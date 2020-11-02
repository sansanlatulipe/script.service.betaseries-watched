# pylint: disable=unused-import

try:
    from xbmc import executeJSONRPC
except ImportError:
    def executeJSONRPC(query):
        return '{"result":{"movies":[],"moviedetails":{}}}'

try:
    from xbmc import log, LOGDEBUG, LOGINFO, LOGWARNING, LOGERROR
except ImportError:
    def log(msg, lvl):
        print(lvl, msg)
    LOGDEBUG = 'DEBUG'
    LOGINFO = 'INFO'
    LOGWARNING = 'WARNING'
    LOGERROR = 'ERROR'

try:
    from xbmcaddon import Addon
except ImportError:
    class Addon:
        def __init__(self):
            self.settings = {
                'bs_login': 'Dev011',
                'bs_password': 'developer',
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
            return self.settings[key]

        def getLocalizedString(self, labelId):
            return 'Message {}'.format(labelId)

try:
    from xbmcgui import Dialog
except ImportError:
    class Dialog:
        def ok(self, heading, text, usemono=False):
            print(heading, ' > ', text)

        def textviewer(self, heading, text, usemono=False):
            print(heading, ' > ', text)

try:
    from simplecache import SimpleCache
except ImportError:
    class SimpleCache:
        def __init__(self):
            self.cached = {}

        def get(self, key):
            return self.cached.get(key)

        def set(self, key, value):
            self.cached[key] = value
