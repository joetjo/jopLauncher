from datetime import timedelta
from tkinter import messagebox

from JopLauncherConstant import JopLauncher
from base.pair import Pair
from basegui.application import GhApp, GhAppSetup
from basegui.columnpanel import GhColumnPanel
from launcher.core.procevent import EventListener
from launcher.gui.gamesession import GameSession


class procGui(EventListener):
    label_width = 40

    def __init__(self, procmgr):
        self.procMgr = procmgr
        self.procMgr.setListener(self)

        GhAppSetup.width = 600
        GhAppSetup.height = 400
        self.app = GhApp("{} - {}".format(JopLauncher.APPNAME, JopLauncher.VERSION))

        # HEADER
        GhApp.createLabel(self.app.header, 0, 0, text="Playing:")
        self.playing = GhApp.createLabel(self.app.header, 0, 1).variable

        # CONTENT
        content_col = GhColumnPanel(self.app.content)

        GhApp.createLabel(content_col.left, 0, 0, text="Last played:")
        self.played = GhApp.createLabel(content_col.right, 0, 0, anchor='e').variable

        GhApp.createLabel(content_col.left, 1, 0, text="Time played:")
        self.playedDuration = GhApp.createLabel(content_col.right, 1, 0, anchor='e').variable

        GhApp.createLabel(content_col.left, 2, 0, text="Previous sessions:")

        self.sessions = []
        for idx in range(0, JopLauncher.MAX_LAST_SESSION_COUNT):
            self.sessions.append(GameSession.create(content_col.right, 2 + idx, 0))
        self.reloadLastSessions()

        # FOOTER
        footer_col = GhColumnPanel(self.app.footer)
        GhApp.createButton(footer_col.left, 0, 0, self.refresh, "refresh")
        GhApp.createButton(footer_col.left, 0, 1, self.ignore, "x")
        self.mapButton = GhApp.createButton(footer_col.left, 0, 2, self.map, "map").variable
        self.cancelButton = GhApp.createButton(footer_col.left, 0, 3, self.cancelmap, "cancel mapping").widget
        self.cancelButton.grid_remove()

        if self.procMgr.testmode:
            GhApp.createLabel(footer_col.right, 0, 0, text="**TEST**")
            self.testgame = GhApp.createEntry(footer_col.right, 0, 1, 20, "jopLauncherTest").variable
            self.testgameButton = GhApp.createButton(footer_col.right, 0, 2, self.test_startstop, "Start").variable
            self.testgameButton.set("Start")

        proc = procmgr.getFirstMonitored()
        if proc is not None:
            self.setPlaying(proc)

        self.app.start()

    def refresh(self):
        self.procMgr.refresh()

    def reloadLastSessions(self):
        idx = 0
        for name in self.procMgr.last_sessions:
            info = self.procMgr.find(name)
            if info is not None:
                self.sessions[idx].set(name, info)
                idx += 1

        for idx2 in range(idx, JopLauncher.MAX_LAST_SESSION_COUNT):
            self.sessions[idx].set()

    def setPlaying(self, proc):
        if proc is None:
            self.playing.set("")
        else:
            self.playing.set(proc.getName())
            self.setPlayedDuration(float(proc.getStoreEntry()["duration"]))

    def setPlayed(self, proc):
        self.played.set("{} | {}".format(proc.getName(), proc.getPlayedTime()))
        self.setPlayedDuration(float(proc.getStoreEntry()["duration"]))

    def setPlayedDuration(self, duration):
        delta = timedelta(seconds=duration)
        self.playedDuration.set(str(delta))

    # Proc listener implementations

    def newGame(self, proc):
        print("New game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(proc)

    def endGame(self, proc):
        print("End game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(None)
        self.setPlayed(proc)
        self.reloadLastSessions()

    def listSelected(self, message):
        selection = []
        names = None
        for g in self.sessions:
            if g.selected:
                selection.append(g)
                if names is None:
                    names = g.name
                else:
                    names = "{}\n- {}".format(names, g.name)

        if len(selection) > 0 and \
                messagebox.askyesno("Please confirm !", "{}:\n- {}".format(message, names)):
            return Pair(selection, names)
        return None

    def ignore(self):
        pair = self.listSelected("Do you really want to ignore theses files: ")
        if pair is not None:
            for g in pair.one:
                g.deselect()
                self.procMgr.ignore(g.name)
            self.reloadLastSessions()

    def map(self):
        if self.mapButton.get() == "apply mapping":
            error = False
            for g in self.sessions:
                if g.selected:
                    mapname = g.mapping.variable.get()
                    if len(mapname) == 0:
                        messagebox.showerror("Empty name !", "set a name for {}".format(g.name))
                    else:
                        self.procMgr.mapname(g.name, mapname)
                        g.deselect()
                        g.disableMapping()
                if not error:
                    self.mapButton.set("apply mapping")
                    self.cancelButton.grid()
        else:
            pair = self.listSelected("Do you really want to map theses files with custom name\n"
                                     " ( use PARENT for parent folder name ): ")
            if pair is not None:
                for g in pair.one:
                    g.enableMapping()
                self.mapButton.set("apply mapping")
                self.cancelButton.grid()

    def cancelmap(self):
        self.mapButton.set("map")
        self.cancelButton.grid_remove()
        for g in self.sessions:
            g.deselect()
            g.disableMapping()

    # TEST MODE PURPOSE ONLY
    def test_startstop(self):
        if len(self.playing.get()) == 0:
            self.procMgr.test_setgame(self.testgame.get())
            self.testgameButton.set("Stop")
        else:
            self.procMgr.test_setgame(None)
            self.testgameButton.set("Start")
