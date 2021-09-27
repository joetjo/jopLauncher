# Copyright 2021 joetjo https://github.com/joetjo/MarkdownHelper
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import threading
import time

from JopLauncherConstant import JopSETUP
from launcher.core.procmgr import ProcMgr
from launcher.gui.gui import procGui
from launcher.log import Log


def background(procmgr):
    sleep_time = 2
    delay = JopSETUP.get(JopSETUP.REFRESH_DELAY) / sleep_time
    Log.info("Core-Thread: Starting auto refresh thread - sleeping delay: {}s".format(delay * sleep_time))
    count = delay
    while not procmgr.shutdown:
        time.sleep(sleep_time)
        if procmgr.shutdown:
            Log.debug("Core-thread: stopping background thread")
            break
        elif count > delay:
            procmgr.refresh()
            count = 0
        else:
            count += 1


def main():
    procmgr = ProcMgr()

    bg = threading.Thread(target=background, args=(procmgr,))
    procGui(procmgr, bg)

    Log.info("GUI Closed, stopping core")
    procmgr.stop()


if __name__ == '__main__':
    main()
