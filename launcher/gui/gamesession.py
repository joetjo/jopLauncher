import subprocess
import threading
from datetime import datetime
from tkinter import DISABLED, NORMAL

from JopLauncherConstant import JopLauncher
from base.fileutil import GhFileUtil
from base.jsonstore import GhStorage
from gridgui.application import GhApp
from gridgui.columnpanel import GhColumnPanel
from gridgui.simplepanel import GhSimplePanel
from launcher.gui.strings import Strings


class GameSession(GhSimplePanel):

    def __init__(self, parent, app, row, col, title_mode=False, sticky="nsew"):
        super().__init__(parent, row, col, sticky)
        self.app = app
        self.session = None
        self.game = None
        self.selected = False
        self.mappingEnabled = False
        self.title_mode = title_mode

        col_panel = GhColumnPanel(self.content)
        main_panel = col_panel.left
        action_panel = col_panel.right

        if not title_mode:
            self.ui_selection_check = GhApp.createCheckbox(main_panel, self.row(), self.col_next(), self.applySelection)
            self.ui_selection_check.widget.grid_remove()
        else:
            self.ui_selection_check = GhApp.createCheckbox(main_panel, self.row(), self.col_next(), self.applySelection)

        self.ui_mapping_entry = GhApp.createEntry(main_panel, self.row(), self.col_next(), 20, "")
        self.ui_mapping_entry.widget.grid_remove()
        self.ui_mapping_entry.variable.set('PARENT')

        self.ui_date_label = GhApp.createLabel(main_panel, self.row(), self.col_next(), width=15, anchor="center",
                                               justify='center')
        if title_mode:
            self.ui_date_label.variable.set(Strings.LAST_LAUNCH)

        self.ui_total_label = GhApp.createLabel(main_panel, self.row(), self.col_next(), width=15, anchor="center",
                                                justify='center')
        if title_mode:
            self.ui_total_label.variable.set(Strings.TOTAL_DURATION)

        self.ui_last_label = GhApp.createLabel(main_panel, self.row(), self.col_next(), width=15, anchor="center",
                                               justify='center')
        if title_mode:
            self.ui_last_label.variable.set(Strings.LAST_DURATION)

        if title_mode:
            self.ui_name_label = GhApp.createLabel(main_panel, self.row(), self.col_next(),
                                                   width=JopLauncher.GAME_NAME_WIDTH)
            self.ui_name_label.variable.set(Strings.GAME_NAME)
        else:
            self.ui_name_label = GhApp.createLabel(main_panel, self.row(), self.col_next())

        # Actions column
        self.row_col_reset(0, 1)

        GhApp.createLabel(action_panel, 0, 0, text="  ", anchor="e")
        self.ui_launch_button = GhApp.createButton(action_panel, self.row(), self.col_next(), self.launchGame, text=">",
                                                   padx=2, anchor="e")
        self.ui_launch_button.widget.grid_remove()
        self.default_bg = self.ui_launch_button.widget.cget('bg')

    @staticmethod
    def setOptionalDateInfo(ui_label, session, info_name):
        val = GhStorage.getValue(session.getGameInfo(), info_name)
        if val is not None:
            ui_label.set(str(datetime.fromtimestamp(int(float(val)))))
        else:
            ui_label.set("-")

    @staticmethod
    def setOptionalDurationInfo(ui_label, session, info_name):
        val = int(float(GhStorage.getValue(session.getGameInfo(), info_name)))
        if val is not None:
            if val < 60:
                ui_label.set("{}s".format(str(val)))
            elif val < 3600:
                minute = int(val / 60)
                second = int(val - (minute * 60))
                ui_label.set("{}m {}s".format(str(minute), str(second)))
            else:
                hour = int(val / 3600)
                minute = int((val - (hour * 3600)) / 60)
                ui_label.set("{}h{}m".format(str(hour), str(minute)))
        else:
            ui_label.set("-")

    def set(self, session=None):
        self.session = session
        if self.session is None:
            self.ui_date_label.variable.set("")
            self.ui_total_label.variable.set("")
            self.ui_last_label.variable.set("")
            self.ui_name_label.variable.set("")
            self.ui_selection_check.widget.grid_remove()
            self.ui_launch_button.widget.grid_remove()
        else:
            self.ui_selection_check.widget.grid()
            GameSession.setOptionalDateInfo(self.ui_date_label.variable, self.session, 'last_session')
            GameSession.setOptionalDurationInfo(self.ui_total_label.variable, self.session, 'duration')
            GameSession.setOptionalDurationInfo(self.ui_last_label.variable, self.session, 'last_duration')
            self.ui_name_label.variable.set(self.session.getName())
            self.ui_launch_button.widget.grid()
            self.setButtonState(self.ui_launch_button.widget, GhFileUtil.fileExist(session.getPath()))

    def getName(self):
        if self.session is None:
            return "-"
        else:
            return self.session.getName()

    def applySelection(self):
        self.selected = self.ui_selection_check.variable.get() == 1
        if not self.selected and self.isMappingInProgress():
            self.disableMapping()
        self.app.notifyEntrySelectionUpdate(self.selected, self.title_mode)

    def setSelected(self, mode):
        self.selected = mode
        if mode:
            self.ui_selection_check.variable.set(1)
        else:
            self.ui_selection_check.variable.set(0)

    def isMappingInProgress(self):
        return self.mappingEnabled;

    def enableMapping(self):
        self.mappingEnabled = True
        self.ui_mapping_entry.widget.grid()
        self.ui_date_label.widget.grid_remove()
        self.ui_total_label.widget.grid_remove()
        self.ui_last_label.widget.grid_remove()
        self.ui_launch_button.widget.grid_remove()
        name = self.session.getName()
        original_name = self.session.getOriginName()
        if name == original_name:
            self.ui_name_label.variable.set(name)
        else:
            self.ui_name_label.variable.set("{} ( real name : {} )".format(name, original_name))

    def disableMapping(self):
        self.mappingEnabled = False
        self.ui_mapping_entry.widget.grid_remove()
        self.ui_date_label.widget.grid()
        self.ui_total_label.widget.grid()
        self.ui_last_label.widget.grid()
        self.ui_launch_button.widget.grid()
        if self.session is not None:
            self.ui_name_label.variable.set(self.session.getName())

    def setButtonState(self, button, state):
        if state:
            button.config(state=NORMAL)
            button.config(bg='white')
        else:
            button.config(bg=self.default_bg)
            button.config(state=DISABLED)

    # ACTIONS !
    def launchGame(self):
        # To be sure no game is running, 1st do a refresh
        self.app.applyRefresh()
        if not self.app.isGameRunning():
            game = self.app.procMgr.find(self.session.getName(), "Game launcher")
            launcher = GhStorage.getValue(game, "launcher")
            if launcher is None:
                exe = [self.session.getPath()]
            else:
                exe = [self.app.procMgr.getLauncher(launcher), self.session.getPath()]
            print("Launching game {} ({}) ".format(self.getName(), exe))
            bg = threading.Thread(target=self.launchGameImpl, args=(exe,))
            bg.start()
        else:
            print("A game is already running, cannot launch {} ".format(self.getName()))

    @staticmethod
    def launchGameImpl(exe):
        subprocess.run(exe)
