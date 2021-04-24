import time
import threading

from launcher.core.procmgr import ProcMgr
from launcher.gui.gui import procGui

REFRESH_DELAY = 60


def background(procmgr):
    print("Starting auto refresh thread - sleeping delay: {}s".format(REFRESH_DELAY))
    while not procmgr.shutdown:
        time.sleep(REFRESH_DELAY)
        procmgr.refresh()


def main():
    procmgr = ProcMgr(True)

    bg = threading.Thread(target=background, args=(procmgr,))
    bg.start()

    procGui(procmgr)

    procmgr.stop()


if __name__ == '__main__':
    main()
