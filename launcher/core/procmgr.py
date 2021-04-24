import time

import psutil
import logging  # This module is thread safe.
import threading

from base.jsonstore import GhStorage
from launcher.core.process import ProcessInfo

LOCAL_STORAGE = 'local_storage.json'
LOCK = threading.Lock()


class ProcMgr:

    def __init__(self):
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
        # last_sessions may not be present
        try:
            self.last_sessions = self.storage.data()["last_sessions"]
        except KeyError:
            self.storage.data()["last_sessions"] = []
            self.storage.save()
            self.last_sessions = self.storage.data()["last_sessions"]

        self.loadPList()

    def setListener(self, event_listener):
        self.eventListener = event_listener

    def loadPList(self):
        self.plist = dict()
        for proc in psutil.process_iter():
            try:
                # Fetch process details as dict
                p = ProcessInfo(proc.as_dict(attrs=['pid', 'name', 'exe']))

                self.plist[p.getPid()] = p
                if p.isGame():
                    if self.pMonitored.get(p.getPid()) is None:
                        try:
                            p.setStoreEntry(self.games[p.getName()])
                        except KeyError:
                            print("Creating game {} within storage".format(p.getName()))
                            self.games[p.getName()] = {"duration": "0"}
                            p.setStoreEntry(self.games[p.getName()])
                            self.storage.save()

                        p.setStarted()
                        self.pMonitored[p.getPid()] = p

                        if self.eventListener is not None:
                            self.eventListener.newGame(p)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                print("--- unable to access process ---" + e)
                pass

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
                self.last_sessions.remove(proc.getName())  # keep only one occurrence of each game
                self.last_sessions.insert(0, proc.getName())
                if len(self.last_sessions) > 10:  # keep only 10 games in last sessions
                    self.last_sessions.pop(9)
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

    def getFirstMonitored(self):
        if len(self.pMonitored) > 0:
            return self.pMonitored[next(iter(self.pMonitored))]
        else:
            return None

    def stop(self):
        self.shutdown = True
