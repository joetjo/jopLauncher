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


# Map Json storage for a session
class Session:

    def __init__(self, json, game_info=None):
        self.json = json
        self.game_info = game_info

    def getName(self):
        return self.json[0]

    def setName(self, name):
        self.json[0] = name

    def getPath(self):
        return self.json[1]

    def getOriginName(self):
        return self.json[2]

    # Only on search result ( not available for session from storage )
    def getGameInfo(self):
        return self.game_info


# encapsulate previous sessions management - List of Session managed
# either in storage ( last sessions )
# either in memory ( search result )
class SessionList:

    # Storage none --> im memory session list ( for search result )
    def __init__(self, storage=None, proc_manager=None):
        self.sessions = []
        self.json_sessions = []
        if storage is not None:
            self.json_sessions = storage.getOrCreate(storage.data(), "last_sessions", [])
            for json in storage.getOrCreate(storage.data(), "last_sessions", []):
                self.sessions.append(Session(json, proc_manager.find(json[0])))
        # set storage after reading session
        self.storage = storage

    def list(self):
        return self.sessions

    # session : Session
    def addSession(self, session):
        if self.storage is None:
            self.sessions.append(session)
        else:
            if self.findSessionByName(session.getName()):
                self.removeSessionByName(session.getName())
            self.sessions.insert(0, session)
            self.json_sessions.insert(0, session.json)

    def findSessionByName(self, name):
        found = None
        for session in self.sessions:
            if session.getName() == name:
                found = session
        return found

    def renameSession(self, name, new_name):
        self.findSessionByName(name).name = new_name
        self.findJsonSessionEntryByName(name)[0] = new_name

    def findJsonSessionEntryByName(self, name):
        found = None
        for session in self.json_sessions:
            if session[0] == name:
                found = session
        return found

    # Returns the removed sessions
    def removeSessionByName(self, name):
        found = self.findSessionByName(name)
        if found is not None:
            self.sessions.remove(found)
            self.json_sessions.remove(self.findJsonSessionEntryByName(name))
        return found


class ProcMgr:

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.process_util = ProcessUtil(test_mode)
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

        self.sessions = SessionList(self.storage, self)
        self.game_mappings = self.storage.getOrCreate(self.storage.data(), "mappings", {})
        self.game_ignored = self.storage.getOrCreate(self.storage.data(), "ignored", [])

        self.loadPList()

    def setListener(self, event_listener):
        self.eventListener = event_listener

    def loadPList(self):
        self.plist = dict()
        for process_name in self.process_util.process_iter():
            # Fetch process details as dict
            p = ProcessInfo(self.process_util.readProcessAttributes(process_name))

            if p is not None:
                self.plist[p.getPid()] = p
                if p.isGame():
                    if not self.isIgnore(p.getName()):
                        p.removeExtension()
                        mapping = GhStorage.getValue(self.game_mappings, p.getName())
                        if mapping is not None:
                            p.forceName(mapping)
                        if self.pMonitored.get(p.getPid()) is None:
                            try:
                                p.setStoreEntry(self.find(p.getName()))
                            except KeyError:
                                # TODO mapping name may be identical to a real other process name - to check
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
                session = Session([proc.getName(), proc.path, proc.getOriginName()], self.find(proc.getName()))
                try:
                    self.removeLastSession(session)  # keep only one occurrence of each game
                except:
                    pass  # Nothing to remove
                self.sessions.addSession(session)

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

    def getSessions(self):
        return self.sessions.list()

    def get(self, pid):
        return self.plist.get(pid)

    # Returns the entry with the exact name provided ( unique )
    def find(self, name):
        try:
            return self.games[name]
        except KeyError:
            print("\n\n!!!\n\nERROR : Game {} not found".format(name))

    # Returns all games with the token in their name within the storage
    def searchInStorage(self, token):
        result = SessionList()
        for game_name in self.games:
            if token in game_name:
                last = self.sessions.findSessionByName(game_name)
                if last is None:
                    # not played in 10 last session
                    last = Session([game_name, "", game_name], self.games[game_name])
                result.addSession(last)
        return result

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
            self.sessions.removeSessionByName(name)
            if name in self.games:
                del self.games[name]
            if name in self.game_mappings:
                del self.game_mappings[name]
            self.storage.save()

    # set or overwrite mapping
    def addMapping(self, session, map_name):
        current_name = session.getName()
        new_name = ProcessInfo.getMapName(session.getPath(), map_name)

        # mapping are always stored using the original name
        self.game_mappings[session.getOriginName()] = map_name

        # update existing session stored with the current name
        self.sessions.renameSession(current_name, new_name)

        # update name in game list
        if current_name in self.games:
            self.games[new_name] = self.games[current_name]
            del self.games[current_name]

        self.storage.save()

    def stop(self):
        self.shutdown = True

    # FOR TEST PURPOSE ONLU
    def test_setGame(self, game):
        self.process_util.test_setGame(game)
