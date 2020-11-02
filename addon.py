import sys
import resources.lib.kernel as kernel

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'authentication':
        kernel.authenticate()
    else:
        kernel.fromScratch()
