import os
import re
from datetime import datetime

from JopLauncherConstant import JopLauncher


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

    def getOriginName(self):
        return self.originName

    def forceName(self, map_name):
        self.name = ProcessInfo.getMapName(self.path, map_name)

    @staticmethod
    def getMapName(path, map_name):
        if map_name == 'PARENT':
            parent = os.path.dirname(path).split(os.path.sep)
            return parent[len(parent) - 1]
        else:
            return map_name

    def removeExtension(self):
        if JopLauncher.GAME_EXTENSION in self.name:
            self.name = self.name[0:self.name.rfind(JopLauncher.GAME_EXTENSION)]

    def getPath(self):
        return self.path

    def isGame(self):
        return self.game

    def gameDetector(self, path):
        return (self.path is not None) and re.search(JopLauncher.GAME_PATTERN, path, re.IGNORECASE)

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
