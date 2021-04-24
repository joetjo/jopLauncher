import os
import re
from datetime import datetime

GENERIC_NAMES = ["nw.exe"]


class ProcessInfo:

    def __init__(self, pinfo):
        self.pinfo = pinfo
        self.pid = pinfo['pid']
        self.name = pinfo['name']
        self.path = pinfo['exe']
        self.originName = self.name

        self.game = self.gameDetector(self.path)
        self.storeEntry = None

        self.started = None
        self.duration = None

    def getPid(self):
        return self.pid

    def getName(self):
        return self.name

    def forceName(self, mapname):
        if mapname == 'PARENT':
            parent=os.path.dirname(self.path).split(os.path.sep)
            self.name = parent[len(parent)-1]
            print("Using PARENT folder name {} instead of {}".format(self.name, self.originName))
        else:
            self.name = mapname
            print("Using custom name {} instead of {}".format(self.name, self.originName))

    def removeExtension(self):
        self.name = self.name[0:self.name.rfind(".exe")]

    def getPath(self):
        return self.path

    def isGame(self):
        return self.game

    def gameDetector(self, path):
        return (self.path is not None) and re.search('jeux', path, re.IGNORECASE)

    def setStarted(self):
        if self.started is None:
            self.started = datetime.now()
        else:
            print("/!\\ Start/Stop error: {} was already known to be started".format(self.name))

    def setStopped(self):
        if self.started is None:
            print("/!\\ Start/Stop error: {} was not known to be started".format(self.name))
        else:
            self.duration = datetime.now() - self.started
            self.started = None
            print("{} has run for {}".format(self.name, self.duration))

        return self.duration

    def getPlayedTime(self):
        return self.duration

    def setStoreEntry(self, entry):
        self.storeEntry = entry

    def getStoreEntry(self):
        return self.storeEntry
