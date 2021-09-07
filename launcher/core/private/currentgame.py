# TODO Use GameProcessHolder in gui instead of process : line 147 ( proc, gui.py )
from launcher.log import Log


class GameProcessHolder:

    def __init__(self, proc=None):
        if proc is None:
            self.pid = 0
            self.process = None
        else:
            self.pid = proc.pid
            self.process = proc.process

    # Started does not mean still running
    def isSet(self):
        return self.pid != 0

    def setProcess(self, process):
        self.pid = process.getPid()
        self.process = process

    def reset(self):
        self.pid = 0
        self.process = None
        Log.debug("CURRENT GAME: reset selection")

    def getName(self):
        if self.process is not None:
            return self.process.getName()
