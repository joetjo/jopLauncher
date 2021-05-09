from datetime import datetime
from tkinter import DISABLED, NORMAL, RIGHT, LEFT

from JopLauncherConstant import JopLauncher, JopSETUP
from base.fileutil import GhFileUtil
from base.jsonstore import GhStorage
from base.launcher import GhLauncher
from gridgui.application import GhApp
from gridgui.columnpanel import GhColumnPanel
from gridgui.simplepanel import GhSimplePanel
from launcher.gui.gameeditpanel import GameEditPanel
from launcher.gui.strings import Strings
from launcher.log import Log


class GameSession(GhSimplePanel):

    def __init__(self, parent, app, row, col, title_mode=False, sticky="nsew"):
        super().__init__(parent, row=row, col=col, sticky=sticky)
        self.app = app
        self.session = None
        self.game = None
        self.selected = False
        self.mappingEnabled = False
        self.title_mode = title_mode
        self.edit_mode = False

        col_panel = GhColumnPanel(self.content)
        main_panel = col_panel.left
        action_panel = col_panel.right

        self.row_col_reset(row, col)

        self.ui_selection_check = GhApp.createCheckbox(main_panel, self.row(),
                                                       self.col_next(), self.applySelection)

        self.ui_mapping_entry = GhApp.createEntry(main_panel, self.row(), self.col_next(), 20, "")
        self.ui_mapping_entry.grid_remove()
        self.ui_mapping_entry.set('PARENT')

        self.ui_date_label = GhApp.createLabel(main_panel, self.row(), self.col_next(), width=15, anchor="center",
                                               justify='center')
        if title_mode:
            self.ui_date_label.set(Strings.LAST_LAUNCH)

        self.ui_total_label = GhApp.createLabel(main_panel, self.row(), self.col_next(), width=15, anchor="center",
                                                justify='center')
        if title_mode:
            self.ui_total_label.set(Strings.TOTAL_DURATION)

        self.ui_last_label = GhApp.createLabel(main_panel, self.row(), self.col_next(), width=15, anchor="center",
                                               justify='center')
        if title_mode:
            self.ui_last_label.set(Strings.LAST_DURATION)

        if title_mode:
            self.ui_name_label = GhApp.createLabel(main_panel, self.row(), self.col_next(),
                                                   width=JopSETUP.get(JopSETUP.GAME_NAME_WIDTH))
            self.ui_name_label.set(Strings.GAME_NAME)
        else:
            self.ui_name_label = GhApp.createLabel(main_panel, self.row_next(), self.col_reset(0))

        # EDIT MODE - LINE 2
        if not self.title_mode:
            self.ui_panel = GameEditPanel(main_panel, self.app, self.row(), self.col_reset(0), colspan=10)
            self.ui_panel.grid_remove()

        # Actions column
        self.row_col_reset(0, 1)

        GhApp.createLabel(action_panel, 0, 0, text=" ", anchor="e")
        self.ui_launch_button = GhApp.createButton(action_panel, self.row(), self.col_next(), self.launchGame, text=">",
                                                   padx=2, anchor="e", image=self.app.icons.PLAY)
        self.ui_launch_button.grid_remove()
        self.default_bg = self.ui_launch_button.cget('bg')

        self.ui_note_button = GhApp.createButton(action_panel, self.row(), self.col_next(), self.launchNote, text="n",
                                                 padx=2, anchor="e", image=self.app.icons.DOCUMENT)
        self.ui_note_button.grid_remove()

        self.ui_store_button = GhApp.createButton(action_panel, self.row(), self.col_next(), self.launchWWW, text="s",
                                                  padx=2, anchor="e", image=self.app.icons.SHOP)
        self.ui_store_button.grid_remove()

        self.ui_tips_button = GhApp.createButton(action_panel, self.row(), self.col_next(), self.launchTips, text="t",
                                                 padx=2, anchor="e", image=self.app.icons.TIPS)
        self.ui_tips_button.grid_remove()

        self.ui_platform_label = GhApp.createLabel(action_panel, self.row(), self.col_next(), justify=LEFT, anchor="e")

    @staticmethod
    def setOptionalDateInfo(ui_label, session, info_name):
        val = GhStorage.getValue(session.getGameInfo(), info_name)
        if val is not None:
            ui_label.set(str(datetime.fromtimestamp(int(float(val)))))
        else:
            ui_label.set("-")

    @staticmethod
    def setOptionalDurationInfo(ui_label, session, info_name):
        try:
            val = int(float(GhStorage.getValue(session.getGameInfo(), info_name)))
        except TypeError:
            val = None
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
            self.ui_date_label.set("")
            self.ui_total_label.set("")
            self.ui_last_label.set("")
            self.ui_name_label.set("")
            self.ui_platform_label.set("")
            self.ui_platform_label.setImage(self.app.icons.VOID, compound=RIGHT)
            self.ui_selection_check.grid_remove()
            self.ui_launch_button.grid_remove()
            self.ui_note_button.grid_remove()
            self.ui_store_button.grid_remove()
            self.ui_tips_button.grid_remove()
        else:
            self.ui_selection_check.grid()
            GameSession.setOptionalDateInfo(self.ui_date_label, self.session, 'last_session')
            GameSession.setOptionalDurationInfo(self.ui_total_label, self.session, 'duration')
            GameSession.setOptionalDurationInfo(self.ui_last_label, self.session, 'last_duration')
            self.ui_name_label.set(self.session.getName())
            self.ui_launch_button.grid()
            if GhFileUtil.fileExist(self.session.getPath()):
                self.setButtonState(self.ui_launch_button, True)
                self.ui_launch_button.setImage(self.app.icons.PLAY)
            else:
                self.setButtonState(self.ui_launch_button, False)
                self.ui_launch_button.setImage(self.app.icons.PLAY_OFF)
            self.ui_note_button.grid()
            self.setButtonState(self.ui_note_button, GhFileUtil.fileExist(self.session.getNote()))
            self.ui_store_button.grid()
            self.setButtonState(self.ui_store_button, len(self.session.getWWW()) > 0)
            self.ui_tips_button.grid()
            self.setButtonState(self.ui_tips_button, len(self.session.getTips()) > 0)
            platform = self.session.getPlatform()
            if platform is not None and len(platform) > 0:
                image = self.app.icons.PLATFORMS[platform]
                self.ui_platform_label.setImage(image, compound=RIGHT)
            else:
                self.ui_platform_label.setImage(self.app.icons.NO_PLATFORM, compound=RIGHT)

    def getName(self):
        if self.session is None:
            return "-"
        else:
            return self.session.getName()

    def applySelection(self):
        self.selected = self.ui_selection_check.get() == 1
        if not self.selected and self.isMappingInProgress():
            self.disableMapping()
        if not self.selected and self.isEditInProgress():
            self.disableEdit()
        self.app.notifyEntrySelectionUpdate(self.selected, self.title_mode)

    def setSelected(self, mode):
        self.selected = mode
        if mode:
            self.ui_selection_check.set(1)
        else:
            self.ui_selection_check.set(0)

    def isMappingInProgress(self):
        return self.mappingEnabled

    def enableMapping(self):
        self.mappingEnabled = True
        self.ui_mapping_entry.grid()
        self.ui_date_label.grid_remove()
        self.ui_total_label.grid_remove()
        self.ui_last_label.grid_remove()
        self.ui_launch_button.grid_remove()
        name = self.session.getName()
        original_name = self.session.getOriginName()
        mapping = self.app.procMgr.getMapping(original_name)
        if mapping is not None:
            self.ui_mapping_entry.set(mapping)
        else:
            self.ui_mapping_entry.set("")
        if name == original_name:
            self.ui_name_label.set(name)
        else:
            self.ui_name_label.set("{} ( real name : {} )".format(name, original_name))

    def disableMapping(self):
        self.mappingEnabled = False
        self.ui_mapping_entry.grid_remove()
        self.ui_date_label.grid()
        self.ui_total_label.grid()
        self.ui_last_label.grid()
        self.ui_launch_button.grid()
        if self.session is not None:
            self.ui_name_label.set(self.session.getName())

    def isEditInProgress(self):
        return self.edit_mode

    def saveEdit(self):
        self.ui_panel.updateStorage()
        self.disableEdit()

    def enableEdit(self):
        self.edit_mode = True
        self.ui_panel.set(self.session)
        self.ui_panel.grid()
        Log.debug("Enable edit mode for {}".format(self.getName()))

    def disableEdit(self):
        self.edit_mode = False
        self.ui_panel.grid_remove()
        Log.debug("Disable edit mode for {}".format(self.getName()))

    def setButtonState(self, button, state):
        if state:
            button.widget.config(state=NORMAL)
            button.widget.config(bg='white')
        else:
            button.widget.config(bg=self.default_bg)
            button.widget.config(state=DISABLED)

    # ACTIONS !
    def launchGame(self):
        # To be sure no game is running, 1st do a refresh
        self.app.applyRefresh()
        if not self.app.isGameRunning():
            launcher = self.session.getLauncher()
            custom = self.session.getCustomCommand()
            if launcher is not None and len(launcher) > 0:
                exe = [self.app.procMgr.getLauncher(launcher), self.session.getPath()]
            elif custom is not None and len(custom) > 0:
                exe = [custom]
            else:
                exe = [self.session.getPath()]
            params = self.session.getParameters().strip()
            if params is not None and len(params) > 0:
                for p in params.split(" "):
                    exe.append(p)
            GhLauncher.launch(self.getName(), exe)
        else:
            Log.info("A game is already running, cannot launch {} ".format(self.getName()))

    def launchNote(self):
        note = self.session.getNote()
        if note is not None and len(note) > 0:
            GhLauncher.launch("note", [JopLauncher.NOTE_EXE, note])

    def launchWWW(self):
        page = self.session.getWWW()
        if page is not None and len(page) > 0:
            GhLauncher.launch("Store", [JopLauncher.URL_EXE, page])

    def launchTips(self):
        page = self.session.getTips()
        if page is not None and len(page) > 0:
            GhLauncher.launch("Tips", [JopLauncher.URL_EXE, page])
