import threading
import time

from JopLauncherConstant import JopSETUP
from launcher.core.procmgr import ProcMgr
from launcher.gui.gui import procGui
from launcher.log import Log


def background(procmgr):
    delay = JopSETUP.get(JopSETUP.REFRESH_DELAY)
    Log.info("Starting auto refresh thread - sleeping delay: {}s".format(delay * 5))
    count = delay
    while not procmgr.shutdown:
        time.sleep(5)
        if not procmgr.shutdown and count > delay:
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
