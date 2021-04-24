import time
import threading

from JopLauncherConstant import JopLauncher
from launcher.core.procmgr import ProcMgr
from launcher.gui.gui import procGui


def background(procmgr):
    print("Starting auto refresh thread - sleeping delay: {}s".format(JopLauncher.REFRESH_DELAY))
    while not procmgr.shutdown:
        time.sleep(JopLauncher.REFRESH_DELAY)
        procmgr.refresh()


def main():
    procmgr = ProcMgr(True)

    bg = threading.Thread(target=background, args=(procmgr,))
    bg.start()

    procGui(procmgr)

    procmgr.stop()


if __name__ == '__main__':
    main()
