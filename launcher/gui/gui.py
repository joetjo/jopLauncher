from datetime import timedelta
from tkinter import messagebox

from JopLauncherConstant import JopLauncher
from base.pair import Pair
from basegui.application import GhApp, GhAppSetup
from basegui.columnpanel import GhColumnPanel
from launcher.core.procevent import EventListener
from launcher.gui.gamesession import GameSession


NO_GAME = "-"


class procGui(EventListener):
    label_width = 40

    def __init__(self, procmgr):
        self.procMgr = procmgr
        self.procMgr.setListener(self)

        self.app = GhApp("{} - {}".format(JopLauncher.APPNAME, JopLauncher.VERSION))

        # HEADER
        header_col = GhColumnPanel(self.app.header)
        GhApp.createLabel(header_col.left, 0, 0, text="Playing:")
        self.ui_playing_label = GhApp.createLabel(header_col.left, 0, 1)
        self.ui_playing_label.variable.set(NO_GAME)

        GhApp.createLabel(header_col.right, 0, 0, text="| Search:")
        self.ui_search_entry = GhApp.createEntry(header_col.right, 0, 1, 20, "", command=self.applySearch)
        self.ui_search_button = GhApp.createButton(header_col.right, 0, 2, self.applySearch, text="go")
        self.ui_search_reset_button = GhApp.createButton(header_col.right, 0, 3, self.applyResetSearch, text="reset")
        self.ui_search_reset_button.widget.grid_remove()

        # CONTENT
        content_col = GhColumnPanel(self.app.content)

        GhApp.createLabel(content_col.left, 0, 0, text="Last played:")
        self.ui_played_label = GhApp.createLabel(content_col.right, 0, 0, anchor='e')

        GhApp.createLabel(content_col.left, 1, 0, text="Time played:")
        self.ui_played_duration_label = GhApp.createLabel(content_col.right, 1, 0, anchor='e')

        self.ui_prev_session_label = GhApp.createLabel(content_col.left, 2, 0)
        self.ui_prev_session_label.variable.set("Previous sessions:")

        self.sessions = []
        for idx in range(0, JopLauncher.MAX_LAST_SESSION_COUNT):
            self.sessions.append(GameSession.create(content_col.right, self, 2 + idx, 0))
        self.reloadLastSessions()
        self.ui_help_label = GhApp.createLabel(content_col.right, JopLauncher.MAX_LAST_SESSION_COUNT, 0)
        self.ui_help_label.variable.set("if name is a specific one but unrelated to game, set a custom name\n"
                                        "if name is a generic launcher, use PARENT to use parent folder name")
        self.ui_help_label.widget.grid_remove()

        # FOOTER
        footer_col = GhColumnPanel(self.app.footer)
        GhApp.createButton(footer_col.left, 0, 0, self.applyRefresh, "refresh")
        GhApp.createLabel(footer_col.left, 0, 1, text=" ")
        self.ui_remove_button = GhApp.createButton(footer_col.left, 0, 2, self.applyIgnore, "x")
        self.ui_mapping_button = GhApp.createButton(footer_col.left, 0, 3, self.applyMapping, "map")
        self.ui_cancel_button = GhApp.createButton(footer_col.left, 0, 4, self.applyCancelMapping, "cancel mapping")
        self.ui_cancel_button.widget.grid_remove()
        self.ui_remove_button.widget.grid_remove()
        self.ui_mapping_button.widget.grid_remove()

        if self.procMgr.testmode:
            GhApp.createLabel(footer_col.right, 0, 0, text="**TEST**")
            self.ui_testgame_entry = GhApp.createEntry(footer_col.right, 0, 1, 20, "jopLauncherTest.exe")
            self.ui_testgame_button = GhApp.createButton(footer_col.right, 0, 2, self.test_startStop, "Start")
            self.ui_testgame_button.variable.set("Start")

        proc = procmgr.getFirstMonitored()
        if proc is not None:
            self.setPlaying(proc)

        self.app.start()

    def applyRefresh(self):
        self.applyResetSearch()
        self.procMgr.refresh()

    def reloadLastSessions(self):
        self.clearAllSessions()
        idx = 0
        for name in self.procMgr.last_sessions:
            info = self.procMgr.find(name)
            if info is not None:
                self.sessions[idx].set(name, info)
                idx += 1

    def clearAllSessions(self):
        for idx in range(0, JopLauncher.MAX_LAST_SESSION_COUNT):
            self.sessions[idx].set()

    def applySearch(self):
        token = self.ui_search_entry.variable.get()
        print("Searching for {}".format(token))
        if len(token) > 0:
            self.ui_prev_session_label.variable.set("Search result:")
            self.ui_search_reset_button.widget.grid()
            self.clearAllSessions()

            idx = 0
            for game in self.procMgr.searchInStorage(token):
                if idx < JopLauncher.MAX_LAST_SESSION_COUNT:
                    self.sessions[idx].set(game.name, game.info)
                idx += 1

            self.ui_help_label.widget.grid()
            if idx >= JopLauncher.MAX_LAST_SESSION_COUNT:
                self.ui_help_label.variable.set("{} games map the current search,\n"
                                                " refine the token for find your game !".format(idx))
            else:
                self.ui_help_label.variable.set("{} game(s) map the current search".format(idx))

    def applyResetSearch(self):
        self.ui_search_entry.variable.set("")
        self.ui_help_label.variable.set("")
        self.ui_search_reset_button.widget.grid_remove()
        self.ui_prev_session_label.variable.set("Previous sessions:")
        self.reloadLastSessions()

    def setPlaying(self, proc):
        if proc is None:
            self.ui_playing_label.variable.set(NO_GAME)
        else:
            self.ui_playing_label.variable.set(proc.getName())
            self.setPlayedDuration(float(proc.getStoreEntry()["duration"]))
            self.ui_played_label.variable.set("{} | {}".format(proc.getName(), proc.getPlayedTime()))

    def setPlayed(self, proc):
        self.ui_played_label.variable.set("{} | {}".format(proc.getName(), proc.getPlayedTime()))
        self.setPlayedDuration(float(proc.getStoreEntry()["duration"]))

    def setPlayedDuration(self, duration):
        delta = timedelta(seconds=duration)
        self.ui_played_duration_label.variable.set(str(delta))

    # BEGIN Proc listener implementations

    def newGame(self, proc):
        print("New game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(proc)

    def endGame(self, proc):
        print("End game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(None)
        self.setPlayed(proc)
        self.reloadLastSessions()

    # END Proc listener implementations

    # BEGIN GameSession listener
    def notifyEntrySelectionUpdate(self):
        if self.isGameSelected():
            self.ui_remove_button.widget.grid()
            self.ui_mapping_button.widget.grid()
        else:
            self.ui_remove_button.widget.grid_remove()
            self.ui_mapping_button.widget.grid_remove()

    # END GameSession listener

    def isGameSelected(self):
        for g in self.sessions:
            if g.selected:
                return True
        return False

    def getGameSelected(self, message=None):
        selection = []
        names = None
        for g in self.sessions:
            if g.selected:
                selection.append(g)
                if names is None:
                    names = g.name
                else:
                    names = "{}\n- {}".format(names, g.name)

        if message is None or \
                (len(selection) > 0 and
                 messagebox.askyesno("Please confirm !", "{}:\n- {}".format(message, names))):
            return Pair(selection, names)
        return None

    def applyIgnore(self):
        pair = self.getGameSelected("Do you really want to ignore theses files: ")
        if pair is not None:
            for g in pair.one:
                g.deselect()
                self.procMgr.applyIgnore(g.name)
            self.reloadLastSessions()

    def applyMapping(self):
        if self.ui_mapping_button.variable.get() == "apply mapping":
            error = False
            for g in self.sessions:
                if g.selected:
                    mapname = g.ui_mapping_entry.variable.get()
                    if len(mapname) == 0:
                        error = True
                        messagebox.showerror("Empty name !", "set a name for {}".format(g.name))
                    else:
                        self.procMgr.mapname(g.name, mapname)
                        g.deselect()
                        g.disableMapping()
            if not error:
                self.ui_mapping_button.variable.set("map")
                self.ui_cancel_button.widget.grid_remove()
                self.ui_help_label.widget.grid_remove()
        else:
            pair = self.getGameSelected()
            if pair is not None:
                for g in pair.one:
                    g.enableMapping()
                self.ui_mapping_button.variable.set("apply mapping")
                self.ui_cancel_button.widget.grid()
                self.ui_help_label.widget.grid()

    def applyCancelMapping(self):
        self.ui_mapping_button.variable.set("map")
        self.ui_cancel_button.widget.grid_remove()
        self.ui_help_label.widget.grid_remove()
        for g in self.sessions:
            g.deselect()
            g.disableMapping()

    # TEST MODE PURPOSE ONLY
    def test_startStop(self):
        if self.ui_playing_label.variable.get() == NO_GAME:
            self.procMgr.test_setgame(self.ui_testgame_entry.variable.get())
            self.ui_testgame_button.variable.set("Stop")
        else:
            self.procMgr.test_setgame(None)
            self.ui_testgame_button.variable.set("Start")
