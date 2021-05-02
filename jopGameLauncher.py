import threading
import time

from JopLauncherConstant import JopLauncher
from launcher.core.procmgr import ProcMgr
from launcher.gui.gui import procGui
from launcher.log import Log


def background(procmgr):
    Log.info("Starting auto refresh thread - sleeping delay: {}s".format(JopLauncher.REFRESH_DELAY * 5))
    count = JopLauncher.REFRESH_DELAY
    while not procmgr.shutdown:
        time.sleep(5)
        if count > JopLauncher.REFRESH_DELAY:
            procmgr.refresh()
            count = 0
        else:
            count += 1


def main():
    procmgr = ProcMgr()

    bg = threading.Thread(target=background, args=(procmgr,))
    bg.start()

    procGui(procmgr)

    procmgr.stop()


if __name__ == '__main__':
    main()
