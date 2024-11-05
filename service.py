import sys
from resources.lib.launcher import Launcher


if __name__ == '__main__':
    launcher = Launcher()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if 'authentication' == command:
            launcher.authenticate()
    else:
        launcher.synchronize()
