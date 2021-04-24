import datetime
import time
# psutil must no be imported --> all call inside ProcessUtil fpr easy test purpose
import logging  # This module is thread safe.
import threading

from JopLauncherConstant import JopLauncher
from base.jsonstore import GhStorage
from launcher.core.private.process import ProcessInfo
from launcher.core.private.processutil import ProcessUtil

LOCAL_STORAGE = 'local_storage.json'
LOCK = threading.Lock()


class ProcMgr:

    def __init__(self, testmode=False):
        self.testmode = testmode
        self.putil = ProcessUtil(testmode)
        self.shutdown = False
        self.plist = dict()
        self.pMonitored = dict()
        self.pStopped = dict()
        self.eventListener = None

        self.storage = GhStorage(LOCAL_STORAGE)
        try:
            self.games = self.storage.data()["Games"]
        except KeyError:
            self.storage.reset({"Games": {}})
            self.games = self.storage.data()["Games"]

        self.last_sessions = self.storage.getOrCreate(self.storage.data(), "last_sessions", [])
        self.game_mappings = self.storage.getOrCreate(self.storage.data(), "mappings", {})
        self.game_ignored = self.storage.getOrCreate(self.storage.data(), "ignored", [])

        self.loadPList()

    def setListener(self, event_listener):
        self.eventListener = event_listener

    def loadPList(self):
        self.plist = dict()
        for proc in self.putil.process_iter():
            # Fetch process details as dict
            p = ProcessInfo(self.putil.readProcessAttributes(proc))

            if p is not None:
                self.plist[p.getPid()] = p
                if p.isGame():
                    if not self.isIgnore(p.getName()):
                        mapping = GhStorage.getValue(self.game_mappings, p.getName())
                        if mapping is not None:
                            p.forceName(mapping)
                        else:
                            p.removeExtension()
                        if self.pMonitored.get(p.getPid()) is None:
                            try:
                                p.setStoreEntry(self.find(p.getName()))
                            except KeyError:
                                print("Creating game {} within storage".format(p.getName()))
                                self.games[p.getName()] = {"duration": "0"}
                                p.setStoreEntry(self.games[p.getName()])
                                self.storage.save()

                            p.setStarted()
                            self.pMonitored[p.getPid()] = p

                            if self.eventListener is not None:
                                self.eventListener.newGame(p)
                    else:
                        print("Process {} with game pattern is ignored {}".format(p.getName(), p.getPath()))

        print("{} processes detected".format(len(self.plist)))

        values = dict(self.pMonitored)
        # copy list before to be able to remove element from list while looping
        # list is supposed to be just one element... ( play one gate at a time )
        for proc in values.values():
            if self.get(proc.getPid()) is None:
                new_duration = proc.setStopped()
                del self.pMonitored[proc.getPid()]
                self.pStopped[proc.getPid()] = proc

                store = proc.getStoreEntry()
                try:
                    duration = float(store["duration"])
                except KeyError:
                    duration = 0.0
                store["duration"] = str(duration + new_duration.total_seconds())
                store["last_duration"] = str(new_duration.total_seconds())
                store["last_session"] = str(time.time())
                try:
                    self.last_sessions.remove(proc.getName())  # keep only one occurrence of each game
                except:
                    pass  # Nothing to remove
                self.last_sessions.insert(0, proc.getName())
                if len(self.last_sessions) > JopLauncher.MAX_LAST_SESSION_COUNT:  # keep only 10 games in last sessions
                    self.last_sessions.pop(JopLauncher.MAX_LAST_SESSION_COUNT - 1)
                self.storage.save()

                if self.eventListener is not None:
                    self.eventListener.endGame(proc)

    def refresh(self):
        if LOCK.acquire(False):  # Non-blocking -- return whether we got it
            print('Refreshing...')
            self.loadPList()
            LOCK.release()
        else:
            logging.info("Couldn't get the lock. Maybe next time")

    def get(self, pid):
        return self.plist.get(pid)

    def find(self, name):
        return self.games[name]

    def getFirstMonitored(self):
        if len(self.pMonitored) > 0:
            return self.pMonitored[next(iter(self.pMonitored))]
        else:
            return None

    def isIgnore(self, name):
        return name in self.game_ignored

    def ignore(self, name):
        if not self.isIgnore(name):
            self.game_ignored.append(name)
            self.last_sessions.remove(name)
            self.storage.save()

    # set or overwrite mapping
    def mapname(self, name, mapname):
        self.game_mappings[name] = mapname
        self.storage.save()

    def stop(self):
        self.shutdown = True

    # FOR TEST PURPOSE ONLU
    def test_setgame(self, game):
        self.putil.test_setgame(game)
