from resources.lib.infra import xbmcmod


def debug(msg):
    xbmcmod.log(msg, xbmcmod.LOGDEBUG)


def info(msg):
    xbmcmod.log(msg, xbmcmod.LOGINFO)


def warn(msg):
    xbmcmod.log(msg, xbmcmod.LOGWARNING)


def error(msg):
    xbmcmod.log(msg, xbmcmod.LOGERROR)
