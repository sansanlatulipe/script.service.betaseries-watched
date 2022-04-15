import sys
from resources.lib.launcher import Launcher


if __name__ == '__main__':
    launcher = Launcher()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'authentication':
            launcher.authenticate()
    else:
        launcher.synchronize()
