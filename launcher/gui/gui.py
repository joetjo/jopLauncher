from datetime import timedelta
from tkinter import messagebox

from JopLauncherConstant import JopLauncher
from base.pair import Pair
from basegui.application import GhApp
from basegui.columnpanel import GhColumnPanel
from launcher.core.procevent import EventListener
from launcher.gui.gamesession import GameSession
from launcher.gui.strings import Strings


class procGui(EventListener):
    label_width = 40

    def __init__(self, procmgr):
        self.ready = False
        self.procMgr = procmgr
        self.search_mode = False
        self.procMgr.setListener(self)

        self.app = GhApp("{} - {}".format(JopLauncher.APP_NAME, JopLauncher.VERSION))

        # HEADER
        header_col = GhColumnPanel(self.app.header)
        GhApp.createLabel(header_col.left, 0, 0, text=Strings.PLAYING)
        self.ui_playing_label = GhApp.createLabel(header_col.left, 0, 1)
        self.ui_playing_label.variable.set(Strings.NO_GAME)

        GhApp.createLabel(header_col.right, 0, 0, text=Strings.SEARCH)
        self.ui_search_entry = GhApp.createEntry(header_col.right, 0, 1, 20, "", command=self.applySearch)
        self.ui_search_button = GhApp.createButton(header_col.right, 0, 2, self.applySearch, text=Strings.SEARCH_ACTION)
        self.ui_search_reset_button = GhApp.createButton(header_col.right, 0, 3, self.applyResetSearch,
                                                         text=Strings.RESET_SEARCH_ACTION)
        self.ui_search_reset_button.widget.grid_remove()

        # CONTENT
        content_col = GhColumnPanel(self.app.content)

        # CONTENT LEFT
        GhApp.createLabel(content_col.left, 0, 0, text=Strings.LAST_PLAYED)
        GhApp.createLabel(content_col.left, 1, 0, text=Strings.TIME_PLAYED)
        self.ui_prev_session_label = GhApp.createLabel(content_col.left, 2, 0)
        self.ui_prev_session_label.variable.set(Strings.PREVIOUS)

        self.ui_help_label = GhApp.createLabel(content_col.left, 3, 0, width=5)
        self.ui_help_label.variable.set(Strings.HELP_MAPPING)
        self.ui_help_label.widget.grid_remove()

        # CONTENT RIGHT
        self.ui_played_label = GhApp.createLabel(content_col.right, 0, 0, anchor='e')
        self.ui_played_duration_label = GhApp.createLabel(content_col.right, 1, 0, anchor='e')

        GameSession.create(content_col.right, self, 2, 0, title_mode=True)
        self.ui_sessions = []
        for idx in range(0, JopLauncher.MAX_LAST_SESSION_COUNT):
            self.ui_sessions.append(GameSession.create(content_col.right, self, 3 + idx, 0))
        self.reloadLastSessions()

        # FOOTER
        footer_col = GhColumnPanel(self.app.footer)
        GhApp.createButton(footer_col.left, 0, 0, self.applyRefresh, Strings.REFRESH_ACTION)
        GhApp.createLabel(footer_col.left, 0, 1, text=" ")
        self.ui_remove_button = GhApp.createButton(footer_col.left, 0, 2, self.applyIgnore, Strings.IGNORE_ACTION)
        self.ui_mapping_button = GhApp.createButton(footer_col.left, 0, 3, self.applyMapping, Strings.MAPPING_ACTION)
        self.ui_cancel_button = GhApp.createButton(footer_col.left, 0, 4, self.applyCancelMapping,
                                                   Strings.MAPPING_CANCEL_ACTION)
        self.ui_cancel_button.widget.grid_remove()
        self.ui_remove_button.widget.grid_remove()
        self.ui_mapping_button.widget.grid_remove()

        if self.procMgr.test_mode:
            GhApp.createLabel(footer_col.right, 0, 0, text="**TEST** ( no extension )")
            self.ui_testgame_entry = GhApp.createEntry(footer_col.right, 0, 1, 20, "FakeGameName")
            self.ui_testgame_button = GhApp.createButton(footer_col.right, 0, 2, self.test_startStop, "Start")
            self.ui_testgame_button.variable.set("Start")
        else:
            GhApp.createLabel(footer_col.right, 0, 0, text=JopLauncher.SHORT_ABOUT)
            GhApp.createButton(footer_col.right, 0, 2, procGui.applyAbout, Strings.ABOUT_ACTION)

        proc = procmgr.getFirstMonitored()
        if proc is not None:
            self.setPlaying(proc)

        self.ready = True
        self.app.start()

    def applyRefresh(self):
        self.applyResetSearch()
        self.procMgr.refresh()

    def reloadLastSessions(self):
        self.clearAllSessions()

        idx = 0
        for session in self.procMgr.getSessions():
            if idx < JopLauncher.MAX_LAST_SESSION_COUNT:
                self.ui_sessions[idx].set(session)
            idx += 1

    def clearAllSessions(self):
        for idx in range(0, JopLauncher.MAX_LAST_SESSION_COUNT):
            self.ui_sessions[idx].set()
        self.notifyEntrySelectionUpdate(False, True)

    def applySearch(self):
        token = self.ui_search_entry.variable.get()
        print("Searching for {}".format(token))
        if len(token) > 0:
            self.search_mode = True
            self.ui_prev_session_label.variable.set(Strings.SEARCHING)
            self.ui_search_reset_button.widget.grid()
            self.clearAllSessions()

            idx = 0
            for session in self.procMgr.searchInStorage(token).list():
                if idx < JopLauncher.MAX_LAST_SESSION_COUNT:
                    self.ui_sessions[idx].set(session)
                idx += 1

            if idx >= JopLauncher.MAX_LAST_SESSION_COUNT:
                self.ui_prev_session_label.variable.set(Strings.RESULT_SEARCH_EXCEED
                                                        .format(idx, JopLauncher.MAX_LAST_SESSION_COUNT))
            else:
                self.ui_prev_session_label.variable.set(Strings.RESULT_SEARCH.format(idx))

    def applyResetSearch(self):
        self.search_mode = False
        self.ui_search_entry.variable.set("")
        self.ui_prev_session_label.variable.set(Strings.PREVIOUS)
        self.ui_search_reset_button.widget.grid_remove()
        self.reloadLastSessions()

    def searchInProgress(self):
        return self.search_mode

    def setPlaying(self, proc):
        if proc is None:
            self.ui_playing_label.variable.set(Strings.NO_GAME)
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
    def notifyEntrySelectionUpdate(self, selected, all_mode):
        if self.ready:
            if all_mode:
                for ui_session in self.ui_sessions:
                    ui_session.setSelected(selected)

            if selected:
                self.ui_remove_button.widget.grid()
                self.ui_mapping_button.widget.grid()
            else:
                self.ui_remove_button.widget.grid_remove()
                self.ui_mapping_button.widget.grid_remove()

    # END GameSession listener

    def isGameSelected(self):
        for ui_session in self.ui_sessions:
            if ui_session.selected:
                return True
        return False

    def getGameSelected(self, message=None):
        selection = []
        names = None
        for ui_session in self.ui_sessions:
            if ui_session.selected:
                selection.append(ui_session)
                if names is None:
                    names = ui_session.getName()
                else:
                    names = "{}\n- {}".format(names, ui_session.getName())

        if message is None or \
                (len(selection) > 0 and
                 messagebox.askyesno(Strings.CONFIRM_TITLE,
                                     Strings.CONFIRM_IGNORE_SELECTION.format(message, names))):
            return Pair(selection, names)
        return None

    def applyIgnore(self):
        pair = self.getGameSelected(Strings.CONFIRM_IGNORE_APPLY)
        if pair is not None:
            for ui_session in pair.one:
                ui_session.setSelected(False)
                self.procMgr.ignore(ui_session.getName())

            if self.searchInProgress():
                self.applySearch()
            else:
                self.reloadLastSessions()

    def applyMapping(self):
        if self.ui_mapping_button.variable.get() == Strings.MAPPING_APPLY_ACTION:
            error = False
            for ui_session in self.ui_sessions:
                if ui_session.selected:
                    map_name = ui_session.ui_mapping_entry.variable.get()
                    if len(map_name) == 0:
                        error = True
                        messagebox.showerror(Strings.EMPTY_NAME.format(ui_session.name))
                    else:
                        self.procMgr.addMapping(ui_session.session, map_name)
                        ui_session.setSelected(False)
                        ui_session.disableMapping()
            if not error:
                self.ui_mapping_button.variable.set(Strings.MAPPING_ACTION)
                self.ui_cancel_button.widget.grid_remove()
                self.ui_help_label.widget.grid_remove()

                if self.searchInProgress():
                    self.applySearch()
                else:
                    self.reloadLastSessions()

        elif self.isGameSelected():
            pair = self.getGameSelected()
            if pair is not None:
                for ui_session in pair.one:
                    ui_session.enableMapping()
                self.ui_mapping_button.variable.set(Strings.MAPPING_APPLY_ACTION)
                self.ui_cancel_button.widget.grid()
                self.ui_help_label.widget.grid()

    def applyCancelMapping(self):
        self.ui_mapping_button.variable.set("map")
        self.ui_cancel_button.widget.grid_remove()
        self.ui_help_label.widget.grid_remove()
        for ui_session in self.ui_sessions:
            ui_session.setSelected(False)
            ui_session.disableMapping()

    @staticmethod
    def applyAbout():
        messagebox.showinfo(JopLauncher.APP_NAME,
                            "Version {}\n\n{} \n{}".format(JopLauncher.VERSION, JopLauncher.SHORT_ABOUT,
                                                           JopLauncher.URL))

    # TEST MODE PURPOSE ONLY
    def test_startStop(self):
        if self.ui_playing_label.variable.get() == Strings.NO_GAME:
            self.procMgr.test_setGame(self.ui_testgame_entry.variable.get())
            self.ui_testgame_button.variable.set("Stop")
        else:
            self.procMgr.test_setGame(None)
            self.ui_testgame_button.variable.set("Start")
