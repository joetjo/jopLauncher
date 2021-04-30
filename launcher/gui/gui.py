import time
from datetime import timedelta
from tkinter import messagebox

from JopLauncherConstant import JopLauncher
from base.pair import Pair
from basegui.application import GhApp
from basegui.appmenu import GhAppMenu
from basegui.columnpanel import GhColumnPanel
from basegui.listnameditempanel import GhListNamedItemPanel
from basegui.simplepanel import GhSimplePanel
from icons.icons import GhIcons
from launcher.core.procevent import EventListener
from launcher.gui.displaymode import DisplayMode
from launcher.gui.gameactionspanel import GameActionPanel
from launcher.gui.gamesession import GameSession
from launcher.gui.strings import Strings


class procGui(EventListener):
    """ Main Application for JopLauncher

    UI widget are called ui_... and GhAppHandle ( Pair Variable / Widget )
    UI callback are called apply....
    """

    HEADER_LABEL_WIDTH = 40

    def __init__(self, procmgr):
        self.ready = False
        self.procMgr = procmgr
        self.procMgr.setListener(self)
        self.last_start = -1
        self.display_mode = DisplayMode(self)

        test_mode = ""
        if procmgr.test_mode:
            test_mode = "- test mode"
        self.app = GhApp("{} - {} {}".format(JopLauncher.APP_NAME, JopLauncher.VERSION, test_mode))
        app = self.app

        self.icons = GhIcons()

        self.menu = GhAppMenu(app.window, app)
        self.menu.add(Strings.MENU_EXCLUDED, self.applyShowExcluded)
        self.menu.add(Strings.MENU_LAUNCHER, self.applyShowLauncher)
        self.menu.addSep()
        self.menu.add(Strings.EXIT, self.applyExit)

        # HEADER
        header_col = GhColumnPanel(self.app.header)

        # HEADER LEFT
        label_width = 8

        # 1st line
        self.ui_menu_button = GhApp.createButton(header_col.left, app.row(), app.col_next(), text="::",
                                                 width=1, padx=0,
                                                 command=self.menu.pop)
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
        # 1st line
        app.row_col_reset()
        GhApp.createLabel(header_col.right, app.row(), app.col_next(), width=15)
        GhApp.createLabel(header_col.right, app.row(), app.col_next(), text=Strings.SEARCH)
        self.ui_search_entry = GhApp.createEntry(header_col.right, app.row(), app.col_next(), 20, "",
                                                 command=self.applySearch)
        self.ui_search_button = GhApp.createButton(header_col.right, app.row_next(), app.col_reset(),
                                                   self.applySearch, text=Strings.SEARCH_ACTION, width=5)

        # 2nd line
        GhApp.createLabel(header_col.right, app.row(), app.col_next(), width=15)
        GhApp.createLabel(header_col.right, app.row(), app.col_next(), text=Strings.FILTER)
        self.filter_panel = GhSimplePanel(header_col.right, app.row_next(), app.col_reset())
        self.ui_installed_filter = GhApp.createCheckbox(self.filter_panel.content, 0, 0,
                                                        text=Strings.INSTALLED_FILTER, command=self.applyFilter)

        # 3rd line
        self.ui_prev_session_label = GhApp.createLabel(header_col.right, app.row(), app.col_reset(3), colspan=3)
        self.ui_prev_session_label.variable.set(self.display_mode.display_mode_string)
        self.ui_search_reset_button = GhApp.createButton(header_col.right,
                                                         app.row(), app.col_next(),
                                                         self.reloadLastSessions,
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
            self.ui_sessions.append(GameSession(content_panel, self, app.row_reset(2 + idx), app.col()))

        # CONTENT RIGHT
        app.row_col_reset()
        self.ui_options = GhListNamedItemPanel(content_col.right, Strings.PLATFORMS, app.row(), app.col(),
                                               command=self.applyRemoveInOptionList, on_close=self.applyCloseExtended)

        # FOOTER
        app.row_col_reset()
        footer_col = GhColumnPanel(self.app.footer)

        # FOOTER LEFT
        if self.procMgr.test_mode:
            print(" ******** TEST MODE DETECTED ********************  USE ABOUT BUTTON !!! ")
            self.test_visible = True
            self.ui_test_game_label = GhApp.createLabel(footer_col.left, app.row(), app.col_next(),
                                                        text="**TEST** ( no extension )")
            self.ui_test_game_entry = GhApp.createEntry(footer_col.left, app.row(), app.col_next(), 20, "FakeGameName")
            self.ui_test_game_button = GhApp.createButton(footer_col.left, app.row(), app.col_next(),
                                                          self.test_startStop, "Start")
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

        self.reloadLastSessions()

        proc = procmgr.getFirstMonitored()
        if proc is not None:
            self.setPlaying(proc)

        self.ready = True
        self.app.start()

    # BACKEND Refresh
    # Restore last session mode and trigger manuel process refresh
    def applyRefresh(self):
        print("UI: cancel search mode if enabled and request process check ( backend )")
        if self.searchInProgress():
            self.reloadLastSessions()
        self.procMgr.refresh()

    # Restore last session mode and trigger manuel process refresh
    def reloadLastSessions(self):
        print("UI: restore last sessions mode and reload")
        self.display_mode.enableLastSessionMode()

        idx = 0
        for session in self.procMgr.getSessions():
            if self.display_mode.isVisible(session):
                if idx < JopLauncher.MAX_LAST_SESSION_COUNT:
                    self.ui_sessions[idx].set(session)
                idx += 1

        self.clearAllSessions(start_index=idx)
        # refresh extended info if needed
        self.display_mode.refreshExtended()

    def clearAllSessions(self, start_index=0):
        print("UI: clearing session list from {}".format(start_index))
        for idx in range(start_index, JopLauncher.MAX_LAST_SESSION_COUNT):
            self.ui_sessions[idx].set()

    def applyFilter(self):
        self.display_mode.filterMode(self.ui_installed_filter.variable.get() == 1)

    def applySearch(self):
        token = self.ui_search_entry.variable.get()
        if len(token) > 0:
            print("Searching for {}".format(token))
            self.display_mode.enableSearchMode()

            print("UI: display search result")
            idx = 0
            for session in self.procMgr.searchInStorage(token).list():
                if self.display_mode.isVisible(session):
                    if idx < JopLauncher.MAX_LAST_SESSION_COUNT:
                        self.ui_sessions[idx].set(session)
                    idx += 1

            self.clearAllSessions(start_index=idx)

            if idx >= JopLauncher.MAX_LAST_SESSION_COUNT:
                self.display_mode.searchResult(
                    Strings.RESULT_SEARCH_EXCEED.format(idx, JopLauncher.MAX_LAST_SESSION_COUNT))
            else:
                self.display_mode.searchResult(Strings.RESULT_SEARCH.format(idx))

    def searchInProgress(self):
        return self.display_mode.isSearchInProgress()

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
        self.display_mode.showPlatforms()

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

            if self.isGameSelected():
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
        self.applyShowExcluded()

    def applyMapping(self):
        if self.ui_game_action_panel.isMappingEnabled():
            error = False
            for ui_session in self.ui_sessions:
                if ui_session.selected:
                    map_name = ui_session.ui_mapping_entry.variable.get()
                    if len(map_name) == 0:
                        error = True
                        messagebox.showerror(Strings.EMPTY_NAME.format(ui_session.getName()))
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
        self.ui_prev_session_label.variable.set(self.display_mode.display_mode_string)
        for ui_session in self.ui_sessions:
            ui_session.disableMapping()
        self.display_mode.refreshSessions()

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

    def applyExit(self):
        self.app.close()

    def applyRemoveInOptionList(self, name):
        if self.display_mode.excluded_mode:
            self.procMgr.removeExcluded(name)
        else:
            self.procMgr.removeLauncher(name)
        self.display_mode.refreshExtended()

    def applyShowExcluded(self):
        self.display_mode.showExcluded()

    def applyShowLauncher(self):
        self.display_mode.showLauncher()

    def applyCloseExtended(self):
        self.display_mode.closeExtended()

    # TEST MODE PURPOSE ONLY
    def test_startStop(self):
        if self.ui_playing_label.variable.get() == Strings.NO_GAME:
            self.procMgr.test_setGame(self.ui_test_game_entry.variable.get())
            self.ui_test_game_button.variable.set("Stop")
        else:
            self.procMgr.test_setGame(None)
            self.ui_test_game_button.variable.set("Start")
