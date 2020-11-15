from resources.lib.launcher import Launcher
from resources.lib.infra.monitor import MyMonitor

if __name__ == '__main__':
    launcher = Launcher()
    monitor = MyMonitor()

    while not monitor.abortRequested():
        launcher.fromLastCheckpoint()
        monitor.waitForAbort(3600)
