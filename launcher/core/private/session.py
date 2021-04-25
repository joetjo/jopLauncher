

# Map Json storage for a session
from launcher.core.private.process import ProcessInfo


class Session:

    def __init__(self, json, game_info=None):
        self.json = json
        self.json[2] = ProcessInfo.removeGameExtension(self.json[2])
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
                self.sessions.append(Session(json, proc_manager.find(json[0], "init session list")))
        # set storage after reading session
        self.storage = storage

    def list(self):
        return self.sessions

    # session : Session - in storage mode, remove existing session for same game before adding
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
