import time
from datetime import timedelta
from tkinter import messagebox, PhotoImage, Image, LEFT, RIGHT

from JopLauncherConstant import JopLauncher
from base.pair import Pair
from basegui.application import GhApp
from basegui.columnpanel import GhColumnPanel
from icons.icons import GhIcons
from launcher.core.procevent import EventListener
from launcher.gui.gameselectedaction import GameActionPanel
from launcher.gui.gamesession import GameSession
from launcher.gui.strings import Strings


class procGui(EventListener):
    HEADER_LABEL_WIDTH = 40

    def __init__(self, procmgr):
        self.ready = False
        self.procMgr = procmgr
        self.search_mode = False
        self.procMgr.setListener(self)
        self.last_start = -1
        self.display_mode = Strings.PREVIOUS

        mode = ""
        if procmgr.test_mode:
            mode = "- test mode"
        self.app = GhApp("{} - {} {}".format(JopLauncher.APP_NAME, JopLauncher.VERSION, mode))
        app = self.app

        self.icons = GhIcons()

        # HEADER
        header_col = GhColumnPanel(self.app.header)

        # HEADER LEFT
        label_width = 8

        # 1st line
        self.ui_menu_button = GhApp.createButton(header_col.left, app.row(), app.col_next(), text="::",
                                                 width=1, padx=0,
                                                 command=self.applyMenu)
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=Strings.PLAYING, width=label_width)
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=":")
        self.ui_playing_label = GhApp.createLabel(header_col.left, app.row_next(), app.col_reset(1))
        self.ui_playing_label.variable.set(Strings.NO_GAME)

        # 2nd line
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=Strings.PLAY_TIME, width=label_width)
        GhApp.createLabel(header_col.left, app.row_next(), app.col_next(), text=":")
        self.ui_play_time_label = GhApp.createLabel(header_col.left, app.row(), app.col_reset(1), anchor='e')

        # 3rd line
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=Strings.TIME_PLAYED, width=label_width)
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=":")
        self.ui_played_duration_label = GhApp.createLabel(header_col.left, app.row_next(), app.col_next(), anchor='e')

        # HEADER RIGHT
        app.row_col_reset()
        GhApp.createLabel(header_col.right, app.row(), app.col_next(), width=15)
        GhApp.createLabel(header_col.right, app.row(), app.col_next(), text=Strings.SEARCH)
        self.ui_search_entry = GhApp.createEntry(header_col.right, app.row(), app.col_next(), 20, "",
                                                 command=self.applySearch)
        self.ui_search_button = GhApp.createButton(header_col.right, app.row_reset(2), app.col_reset(1),
                                                   self.applySearch, text=Strings.SEARCH_ACTION, width=5)

        GhApp.createLabel(header_col.right, app.row_next(), app.col_reset(), text=" ")

        self.ui_prev_session_label = GhApp.createLabel(header_col.right, app.row(), app.col_reset(3), colspan=3)
        self.ui_prev_session_label.variable.set(self.display_mode)
        self.ui_search_reset_button = GhApp.createButton(header_col.right,
                                                         app.row(), app.col_next(),
                                                         self.applyResetSearch,
                                                         text=Strings.RESET_SEARCH_ACTION, width=5)
        self.ui_search_reset_button.widget.grid_remove()

        # CONTENT
        content_col = GhColumnPanel(self.app.content)
        content_panel = content_col.left

        # CONTENT RIGHT
        app.row_col_reset()
        GameSession(content_panel, self, app.row_next(), app.col(), title_mode=True)
        self.ui_sessions = []
        for idx in range(0, JopLauncher.MAX_LAST_SESSION_COUNT):
            self.ui_sessions.append(GameSession(content_panel, self, app.row_reset(1 + idx), app.col()))
        self.reloadLastSessions()

        # FOOTER
        app.row_col_reset()
        footer_col = GhColumnPanel(self.app.footer)

        # FOOTER LEFT
        if self.procMgr.test_mode:
            print(" ******** TEST MODE DETECTED ********************  USE ABOUT BUTTON !!! ")
            self.test_visible = True
            self.ui_test_game_label = GhApp.createLabel(footer_col.left, app.row(), app.col_next(), text="**TEST** ( no extension )")
            self.ui_test_game_entry = GhApp.createEntry(footer_col.left, app.row(), app.col_next(), 20, "FakeGameName")
            self.ui_test_game_button = GhApp.createButton(footer_col.left, app.row(), app.col_next(), self.test_startStop, "Start")
            self.ui_test_game_button.variable.set("Start")
            self.applyAbout()

        GhApp.createButton(footer_col.left, app.row(), app.col_next(), self.applyRefresh,
                           Strings.REFRESH_ACTION, image=self.icons.REFRESH)
        GhApp.createLabel(footer_col.left, app.row(), app.col_next(), text=" ")
        self.ui_game_action_panel = GameActionPanel(footer_col.left, self, app.row(), 5)
        self.ui_game_action_panel.grid_remove()

        # FOOTER RIGHT
        app.row_col_reset()
        GhApp.createLabel(footer_col.right, app.row(), app.col_next(), text=JopLauncher.SHORT_ABOUT)
        GhApp.createButton(footer_col.right, app.row(), app.col_next(), self.applyAbout, Strings.ABOUT_ACTION)

        proc = procmgr.getFirstMonitored()
        if proc is not None:
            self.setPlaying(proc)

        self.ready = True
        self.app.start()

    def applyMenu(self):
        pass # TODO

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
                self.display_mode = Strings.RESULT_SEARCH_EXCEED.format(idx, JopLauncher.MAX_LAST_SESSION_COUNT)
            else:
                self.display_mode = (Strings.RESULT_SEARCH.format(idx))
            self.ui_prev_session_label.variable.set(self.display_mode)

    def applyResetSearch(self):
        self.search_mode = False
        self.display_mode = Strings.PREVIOUS
        self.ui_search_entry.variable.set("")
        self.ui_prev_session_label.variable.set(self.display_mode)
        self.ui_search_reset_button.widget.grid_remove()
        self.reloadLastSessions()

    def searchInProgress(self):
        return self.search_mode

    def setPlaying(self, proc):
        if proc is None:
            self.last_start = -1
            self.ui_play_time_label.variable.set("")
            self.ui_playing_label.variable.set(Strings.NO_GAME)
            self.ui_played_duration_label.variable.set("")
        else:
            self.last_start = time.time()
            self.ui_playing_label.variable.set(proc.getName())
            self.ui_play_time_label.variable.set("just launch !")
            if proc.hasData():
                self.setPlayedDuration(float(proc.getStoreEntry()["duration"]))
            else:
                self.setPlayedDuration(0)

    def setPlayedDuration(self, duration):
        delta = timedelta(seconds=duration)
        self.ui_played_duration_label.variable.set(str(delta))

    # BEGIN Proc listener implementations

    def newGame(self, proc):
        print("New game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(proc)

    def refreshDone(self):
        if self.last_start > 0:
            duration = int((time.time() - self.last_start) / 60)
            self.ui_play_time_label.variable.set("~{} minutes".format(duration))

    def endGame(self, proc):
        print("End game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(None)
        self.reloadLastSessions()

    # END Proc listener implementations

    # BEGIN GameSession listener
    def notifyEntrySelectionUpdate(self, selected, all_mode):
        if self.ready:
            if all_mode:
                for ui_session in self.ui_sessions:
                    ui_session.setSelected(selected)

            if selected:
                self.ui_game_action_panel.grid()
            else:
                self.ui_game_action_panel.grid_remove()

    # END GameSession listener

    def isGameSelected(self):
        for ui_session in self.ui_sessions:
            if ui_session.selected:
                return True
        return False

    def isGameRunning(self):
        return self.last_start > 0

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

    def applyIgnoreOrRemove(self, message, action):
        pair = self.getGameSelected(message)
        if pair is not None:
            for ui_session in pair.one:
                ui_session.setSelected(False)
                action(ui_session.getName())

            if self.searchInProgress():
                self.applySearch()
            else:
                self.reloadLastSessions()

    def applyRemove(self):
        self.applyIgnoreOrRemove(Strings.CONFIRM_REMOVE_APPLY, self.procMgr.remove)

    def applyIgnore(self):
        self.applyIgnoreOrRemove(Strings.CONFIRM_IGNORE_APPLY, self.procMgr.ignore)

    def applyMapping(self):
        if self.ui_game_action_panel.isMappingEnabled():
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
                self.ui_game_action_panel.grid_remove()

                if self.searchInProgress():
                    self.applySearch()
                else:
                    self.reloadLastSessions()

        elif self.isGameSelected():
            pair = self.getGameSelected()
            if pair is not None:
                for ui_session in pair.one:
                    ui_session.enableMapping()
                self.ui_game_action_panel.enableMapping()
                self.ui_prev_session_label.variable.set(Strings.HELP_MAPPING)

    def applyCancelMapping(self):
        self.ui_game_action_panel.disableMapping()
        self.ui_prev_session_label.variable.set(self.display_mode)
        for ui_session in self.ui_sessions:
            ui_session.setSelected(False)
            ui_session.disableMapping()

    def applyAbout(self):
        if self.procMgr.test_mode:
            if self.test_visible:
                self.test_visible = False
                self.ui_test_game_label.widget.grid_remove()
                self.ui_test_game_entry.widget.grid_remove()
                self.ui_test_game_button.widget.grid_remove()
            else:
                self.test_visible = True
                self.ui_test_game_label.widget.grid()
                self.ui_test_game_entry.widget.grid()
                self.ui_test_game_button.widget.grid()
        else:
            messagebox.showinfo(JopLauncher.APP_NAME,
                                "Version {}\nDB Version {}\n\n{} \n{}".format(JopLauncher.VERSION,
                                                                              JopLauncher.DB_VERSION,
                                                                              JopLauncher.SHORT_ABOUT,
                                                                              JopLauncher.URL))

    # TEST MODE PURPOSE ONLY
    def test_startStop(self):
        if self.ui_playing_label.variable.get() == Strings.NO_GAME:
            self.procMgr.test_setGame(self.ui_test_game_entry.variable.get())
            self.ui_test_game_button.variable.set("Stop")
        else:
            self.procMgr.test_setGame(None)
            self.ui_test_game_button.variable.set("Start")
