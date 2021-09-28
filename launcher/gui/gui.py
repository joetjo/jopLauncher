# Copyright 2021 joetjo https://github.com/joetjo/MarkdownHelper
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import time
from datetime import timedelta, datetime
from tkinter import LEFT

from JopLauncherConstant import JopLauncher, JopSETUP
from base.fileutil import GhFileUtil
from base.launcher import GhLauncher
from base.pair import Pair
from basegui.messagebox import GhMessageBox
from gridgui.application import GhApp
from gridgui.columnpanel import GhColumnPanel
from gridgui.listnameditempanel import GhListNamedItemPanel
from gridgui.simplepanel import GhSimplePanel
from icons.icons import GhIcons
from launcher.core.procevent import EventListener
from launcher.gui.displaymode import DisplayMode
from launcher.gui.gameactionspanel import GameActionPanel
from launcher.gui.gamesession import GameSession
from launcher.gui.menu import MainMenu
from launcher.gui.strings import Strings
from launcher.log import Log
from markdown.markdown import MarkdownHelper


class procGui(EventListener):
    """ Main Application for JopLauncher

    UI widget are called ui_... and GhAppHandle ( Pair Variable / Widget )
    UI callback are called apply....
    """

    HEADER_LABEL_WIDTH = 40

    def __init__(self, procmgr, bgthread):
        self.ready = False
        self.procMgr = procmgr
        self.procMgr.setListener(self)
        self.max_session_count = JopSETUP.get(JopSETUP.MAX_LAST_SESSION_COUNT)
        self.last_start = -1
        self.last_start_time = None
        self.display_mode = DisplayMode(self)
        self.discord = True

        self.app = GhApp("{} - {}".format(JopLauncher.APP_NAME, JopLauncher.VERSION), self.applyExit)
        app = self.app

        self.icons = GhIcons(JopLauncher.GAME_PLATFORMS)

        self.menu = MainMenu(app.window, app, self)

        # HEADER
        header_col = GhColumnPanel(self.app.header)

        # HEADER LEFT
        label_width = 8

        # 1st line
        self.ui_menu_button = GhApp.createButton(header_col.left, app.row(), app.col_next(), text="::",
                                                 padx=0, image=self.icons.MENU,
                                                 command=self.menu.pop)
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=Strings.PLAYING, width=label_width)
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=":")
        self.ui_playing_label = GhApp.createLabel(header_col.left, app.row_next(), app.col_reset(1))
        self.ui_playing_label.set(Strings.NO_GAME)

        # 2nd line
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=Strings.PLAY_TIME, width=label_width)
        GhApp.createLabel(header_col.left, app.row(), app.col_next(), text=":")
        self.ui_play_time_label = GhApp.createLabel(header_col.left, app.row_next(), app.col_reset(), anchor='e')

        # 3rd line
        self.ui_discord_button = GhApp.createButton(header_col.left, app.row(), app.col(), text="::",
                                                    padx=0, image=self.icons.DISCORD,
                                                    command=self.applyLaunchDiscord)
        self.ui_discord_label = GhApp.createLabel(header_col.left, app.row(), app.col_next(),
                                                  justify=LEFT, anchor="e")
        self.ui_discord_label.setImage(self.icons.DISCORD, compound=LEFT)
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
                                                   self.applySearch, text=Strings.SEARCH_ACTION,
                                                   image=self.icons.SEARCH)

        # 2nd line
        GhApp.createLabel(header_col.right, app.row(), app.col_next(), width=15)
        GhApp.createLabel(header_col.right, app.row(), app.col_next(), text=Strings.FILTER)
        self.filter_panel = GhSimplePanel(header_col.right, app.row_next(), app.col_reset())
        self.ui_installed_filter = GhApp.createCheckbox(self.filter_panel.content, 0, 0,
                                                        text=Strings.INSTALLED_FILTER, command=self.applyFilter)

        # 3rd line
        self.ui_prev_session_label = GhApp.createLabel(header_col.right, app.row(), app.col_reset(3), colspan=3)
        self.ui_prev_session_label.set(self.display_mode.display_mode_string)
        self.ui_search_reset_button = GhApp.createButton(header_col.right,
                                                         app.row(), app.col_next(),
                                                         self.reloadLastSessions, image=self.icons.SEARCH_RESET,
                                                         text=Strings.RESET_SEARCH_ACTION)
        self.ui_search_reset_button.grid_remove()

        # CONTENT
        content_col = GhColumnPanel(self.app.content)
        content_panel = content_col.left

        # CONTENT RIGHT
        app.row_col_reset()
        GameSession(content_panel, self, app.row_next(), app.col(), title_mode=True)
        self.ui_sessions = []
        for idx in range(0, self.max_session_count):
            self.ui_sessions.append(GameSession(content_panel, self, app.row_reset(2 + idx), app.col()))

        # CONTENT RIGHT
        app.row_col_reset()
        self.ui_options = GhListNamedItemPanel(content_col.right, Strings.PLATFORMS, app.row(), app.col(),
                                               command=self.applyRemoveInOptionList, on_close=self.applyCloseExtended,
                                               images=self.icons.PLATFORMS, close_image=self.icons.CLOSE,
                                               remove_image=self.icons.REMOVE)

        # FOOTER
        app.row_col_reset()
        footer_col = GhColumnPanel(self.app.footer)

        # FOOTER LEFT
        GhApp.createButton(footer_col.left, app.row(), app.col_next(), self.applyRefresh,
                           Strings.REFRESH_ACTION, image=self.icons.REFRESH)
        GhApp.createLabel(footer_col.left, app.row(), app.col_next(), text=" ")
        self.ui_game_action_panel = GameActionPanel(footer_col.left, self, app.row(), 5)
        self.ui_game_action_panel.grid_remove()

        # FOOTER RIGHT
        app.row_col_reset()
        self.ui_status = GhApp.createLabel(footer_col.right, app.row(), app.col_next())
        self.ui_game_stat = GhApp.createLabel(footer_col.right, app.row(), app.col_next())
        GhApp.createButton(footer_col.right, app.row(), app.col_next(), self.applyAbout, Strings.ABOUT_ACTION,
                           image=self.icons.ABOUT)

        self.setDiscord(False)
        self.reloadLastSessions()

        self.setPlaying(procmgr.getCurrentGame())

        self.ready = True

        bgthread.start()
        self.app.start()

    def getWindow(self):
        return self.app.window

    # BACKEND Refresh
    # Restore last session mode and trigger manuel process refresh
    def applyRefresh(self):
        Log.debug("UI: cancel search mode if enabled and request process check ( backend )")
        if self.searchInProgress():
            self.reloadLastSessions()
        self.procMgr.refresh()

    # Restore last session mode and trigger manuel process refresh
    def reloadLastSessions(self):
        Log.debug("UI: restore last sessions mode and reload")
        self.display_mode.enableLastSessionMode()

        idx = 0
        Log.debug("Loading sessions :")
        for session in self.procMgr.getSessions():
            Log.debug(" | {:02d} | {}".format(idx, session.getName()))
            if self.display_mode.isVisible(session):
                if idx < self.max_session_count:
                    self.ui_sessions[idx].set(session)
                idx += 1

        self.clearAllSessions(start_index=idx)
        # refresh extended info if needed
        self.display_mode.refreshExtended()
        self.refreshGameCount()

    def setDiscord(self, discord_flag):
        if self.discord != discord_flag:
            self.discord = discord_flag
            if discord_flag:
                self.ui_discord_button.grid_remove()
                self.ui_discord_label.grid()
            else:
                self.ui_discord_button.grid()
                self.ui_discord_label.grid_remove()

    def clearAllSessions(self, start_index=0):
        Log.debug("UI: clearing session list from {}".format(start_index))
        for idx in range(start_index, self.max_session_count):
            self.ui_sessions[idx].set()

    def applyFilter(self):
        self.display_mode.filterMode(self.ui_installed_filter.get() == 1)

    def applySearch(self):
        token = self.ui_search_entry.get()
        if len(token) > 0:
            Log.debug("Searching for {}".format(token))
            self.display_mode.enableSearchMode()

            Log.debug("UI: display search result")
            idx = 0
            for session in self.procMgr.searchInStorage(token).list():
                if self.display_mode.isVisible(session):
                    if idx < JopSETUP.get(JopSETUP.MAX_LAST_SESSION_COUNT):
                        self.ui_sessions[idx].set(session)
                    idx += 1

            self.clearAllSessions(start_index=idx)

            if idx >= JopSETUP.get(JopSETUP.MAX_LAST_SESSION_COUNT):
                self.display_mode.searchResult(
                    Strings.RESULT_SEARCH_EXCEED.format(idx, JopSETUP.get(JopSETUP.MAX_LAST_SESSION_COUNT)))
            else:
                self.display_mode.searchResult(Strings.RESULT_SEARCH.format(idx))

    def searchInProgress(self):
        return self.display_mode.isSearchInProgress()

    def setPlaying(self, game):
        if game is None or not game.isSet():
            self.last_start = -1
            self.last_start_time = None
            self.ui_play_time_label.set("")
            self.ui_playing_label.set(Strings.NO_GAME)
            self.ui_played_duration_label.set("")
        else:
            now = datetime.now()
            self.last_start = time.time()
            self.last_start_time = now.strftime("%H:%M:%S")
            self.ui_playing_label.set(game.getName())
            self.ui_play_time_label.set("just launch ! ({})".format(self.last_start_time))
            if game.process.hasData():
                self.setPlayedDuration(float(game.process.getStoreEntry()["duration"]))
            else:
                self.setPlayedDuration(0)

    def setPlayedDuration(self, duration):
        delta = timedelta(seconds=duration)
        self.ui_played_duration_label.set(str(delta))

    # BEGIN Proc listener implementations

    def newGame(self, game):
        Log.debug("New game detected {} ({})".format(game.getName(), game.process.getPath()))
        self.setPlaying(game)
        self.reloadLastSessions()

    def refreshDone(self, current_game, platform_list_updated, others):
        if self.last_start_time is not None:
            duration = int((time.time() - self.last_start) / 60)
            self.ui_play_time_label.set("{} | ~{} minutes".format(self.last_start_time, duration))
        now = datetime.now()
        self.ui_status.set("process check @ {}  | ".format(now.strftime("%H:%M:%S")))
        if platform_list_updated:
            self.display_mode.refreshExtended()
        self.setDiscord(JopLauncher.COM_APP_DISCORD in others)

    def refreshGameCount(self):
        self.ui_game_stat.set(Strings.GAME_COUNT.format(len(self.procMgr.games)))

    def endGame(self, proc):
        Log.debug("End game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(None)
        self.reloadLastSessions()

    # END Proc listener implementations

    # BEGIN GameSession listener
    def notifyEntrySelectionUpdate(self, selected, all_mode):
        if self.ready:
            if all_mode:
                for ui_session in self.ui_sessions:
                    if ui_session.session is not None:
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

    def getGameSelected(self, check_current_game=True):
        # No selection can be taken into account while a game is running
        if check_current_game and self.procMgr.currentGame.isSet():
            return None
        selection = []
        names = None
        for ui_session in self.ui_sessions:
            if ui_session.selected and ui_session.getName() is not None:
                selection.append(ui_session)
                if names is None:
                    names = ui_session.getName()
                else:
                    names = "{}\n- {}".format(names, ui_session.getName())

        if len(selection) > 0:
            return Pair(selection, names)
        return None

    def applyIgnoreOrRemove(self, message, action):
        pair = self.getGameSelected()
        if pair is not None:
            height = 100 + ((len(pair.two) - 1) * 1)
            GhMessageBox(self.app.window,
                         Strings.CONFIRM_TITLE,
                         Strings.CONFIRM_IGNORE_SELECTION.format(message, pair.two),
                         message_type=GhMessageBox.QUESTION, height=height,
                         on_ok=lambda: self.applyConfirmIgnoreOrRemoveCallback(pair, action)).show()

    def applyConfirmIgnoreOrRemoveCallback(self, pair, action):
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

    def isEditInProgress(self):
        return self.ui_game_action_panel.isEditEnabled()

    def applyEdit(self):
        if self.isEditInProgress():
            for ui_session in self.ui_sessions:
                if ui_session.selected:
                    ui_session.saveEdit()
                    ui_session.setSelected(False)

                self.ui_game_action_panel.grid_remove()

            self.procMgr.storage.save()
            if self.searchInProgress():
                self.applySearch()
            else:
                self.reloadLastSessions()

        elif self.isGameSelected():
            pair = self.getGameSelected()
            if pair is not None:
                if self.isMappingInProgress():
                    self.applyCancelMapping()
                for ui_session in pair.one:
                    ui_session.enableEdit()
                self.ui_game_action_panel.enableEdit()

    def applyCancelEdit(self):
        self.ui_game_action_panel.disableEdit()
        for ui_session in self.ui_sessions:
            ui_session.disableEdit()
        self.display_mode.refreshSessions()

    def isMappingInProgress(self):
        return self.ui_game_action_panel.isMappingEnabled()

    def applyMapping(self):
        if self.isMappingInProgress():
            error = False
            for ui_session in self.ui_sessions:
                if ui_session.selected:
                    map_name = ui_session.ui_mapping_entry.get()
                    if len(map_name) == 0:
                        error = True
                        GhMessageBox(self.app.window,
                                     Strings.ERROR_INPUT,
                                     Strings.EMPTY_NAME.format(ui_session.getName()),
                                     message_type=GhMessageBox.WARNING).show()
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
                if self.isEditInProgress():
                    self.applyCancelEdit()
                for ui_session in pair.one:
                    ui_session.enableMapping()
                self.ui_game_action_panel.enableMapping()
                self.ui_prev_session_label.set(Strings.HELP_MAPPING)
                self.ui_game_action_panel.disableEdit()

    def applyCancelMapping(self):
        self.ui_game_action_panel.disableMapping()
        self.ui_prev_session_label.set(self.display_mode.display_mode_string)
        for ui_session in self.ui_sessions:
            ui_session.disableMapping()
        self.display_mode.refreshSessions()

    def applyAbout(self):
        message = "{}\n\nVersion {}\nDB Version {}\n\n{} \n{}\nIcons: {}".format(JopLauncher.ABOUT,
                                                                                 JopLauncher.VERSION,
                                                                                 JopLauncher.DB_VERSION,
                                                                                 JopLauncher.SHORT_ABOUT,
                                                                                 JopLauncher.URL,
                                                                                 JopLauncher.ICON_URL)
        GhMessageBox(self.app.window, JopLauncher.APP_NAME, message, width=300, height=220).show()

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

    def applyLaunchPlatform(self, label, cmd):
        self.procMgr.refresh()
        if label not in self.procMgr.platforms:
            GhLauncher.launch(label, cmd, GhFileUtil.parentFolder(cmd[0]))
        else:
            Log.info("Platform {} already running".format(label))

    @staticmethod
    def applyLaunchCompApp():
        GhLauncher.launch("note", JopSETUP.get(JopSETUP.COMPANION_APP))

    @staticmethod
    def updateMarkdownReport():
        MarkdownHelper().markdown()

    @staticmethod
    def applyLaunchIconExtract():
        GhLauncher.launch("icofx", JopSETUP.get(JopSETUP.ICONFX_APP))

    @staticmethod
    def applyLaunchDiscord():
        GhLauncher.launch("discord", JopSETUP.get(JopSETUP.DISCORD))
