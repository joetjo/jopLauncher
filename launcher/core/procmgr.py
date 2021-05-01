# psutil must no be imported --> all call inside ProcessUtil fpr easy test purpose
import logging  # This module is thread safe.
import threading
import time

from JopLauncherConstant import JopLauncher
from base.jsonstore import GhStorage
from launcher.core.migrations.migrate import StorageVersion
from launcher.core.private.process import ProcessInfo
from launcher.core.private.processutil import ProcessUtil
from launcher.core.private.session import SessionList, Session
from launcher.log import Log

LOCAL_STORAGE = 'local_storage.json'
LOCK = threading.Lock()


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
        StorageVersion.check_migration(self.storage, JopLauncher.DB_VERSION)

        try:
            self.games = self.storage.data()["Games"]
        except KeyError:
            self.storage.reset({"Games": {}})
            self.games = self.storage.data()["Games"]

        self.sessions = SessionList(self.storage, self)
        self.game_mappings = self.storage.getOrCreate("mappings", {})
        self.game_ignored = self.storage.getOrCreate("ignored", [])
        self.game_launchers = self.storage.getOrCreate("launchers", {})

        # Running platforms
        self.platforms = []
        self.games_platforms = [""]
        for key in JopLauncher.GAME_PLATFORMS:
            self.games_platforms.append(JopLauncher.GAME_PLATFORMS[key])

        self.loadPList()

    def setListener(self, event_listener):
        self.eventListener = event_listener

    def loadPList(self):
        self.plist = dict()
        platforms = []
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
                            store_entry = self.find(p.getName(), "loading plist: process discovery")
                            if store_entry is None:
                                # TODO mapping name may be identical to a real other process name - to check
                                Log.info("New game discovered : creating game {} within storage".format(p.getName()))
                                self.games[p.getName()] = {"duration": "0"}
                                p.setStoreEntry(self.games[p.getName()])
                                self.storage.save()
                            else:
                                p.setStoreEntry(store_entry)

                            p.setStarted()
                            self.pMonitored[p.getPid()] = p

                            if self.eventListener is not None:
                                self.eventListener.newGame(p)
                    else:
                        Log.debug("Process {} with game pattern is ignored {}".format(p.getName(), p.getPath()))
                elif p.game_platform is not None:
                    if p.game_platform not in platforms:
                        platforms.append(p.game_platform)

        Log.debug("{} processes detected / {} game(s) platforms".format(len(self.plist), len(platforms)))
        self.platforms = platforms
        if self.eventListener is not None:
            self.eventListener.refreshDone()

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
                session = Session([proc.getName(), proc.path, proc.getOriginName()],
                                  self.find(proc.getName(), "loading plist: processing end process"))
                self.sessions.addSession(session)

                self.storage.save()

                if self.eventListener is not None:
                    self.eventListener.endGame(proc)

    def refresh(self):
        if LOCK.acquire(False):  # Non-blocking -- return whether we got it
            Log.debug('Refreshing...')
            self.loadPList()
            LOCK.release()
        else:
            logging.info("Couldn't get the lock. Maybe next time")

    def getSessions(self):
        return self.sessions.list()

    def get(self, pid):
        return self.plist.get(pid)

    # Returns the entry with the exact name provided ( unique )
    def find(self, name, context):
        try:
            return self.games[name]
        except KeyError:
            Log.debug("{} - Warning : Game {} not found (ok if 1st run only)".format(context, name))
            return None

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

    def remove(self, name):
        session = self.sessions.removeSessionByName(name)
        if name in self.games:
            del self.games[name]
        if session is not None and session.getOriginName() in self.game_mappings:
            mapping = self.game_mappings[session.getOriginName()]
            if mapping != 'PARENT':
                del self.game_mappings[name]
        self.storage.save()

    def removeExcluded(self, name):
        if self.isIgnore(name):
            self.game_ignored.remove(name)
            self.storage.save()

    def ignore(self, name):
        if not self.isIgnore(name):
            self.remove(name)
            self.game_ignored.append(name)
            self.storage.save()

    def isLauncher(self, name):
        return GhStorage(self.game_launchers, name) is not None

    def removeLauncher(self, name):
        if self.isLauncher(name):
            del self.game_launchers[name]
            self.storage.save()

    def addLauncher(self, name, path):
        if not self.isIgnore(name):
            self.game_launchers[name] = path
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

    def getLauncher(self, name):
        return GhStorage.getValue(self.game_launchers, name)

    def getLaunchers(self):
        result = [""]
        for key in self.game_launchers:
            result.append(key)
        return result

    def getRunningPlatforms(self):
        return self.platforms

    def getPossiblePlatforms(self):
        return self.games_platforms

    def stop(self):
        self.shutdown = True

    # FOR TEST PURPOSE ONLY
    def test_setGame(self, game):
        self.process_util.test_setGame(game)
