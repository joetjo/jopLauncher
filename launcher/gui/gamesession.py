from datetime import datetime, timedelta
from tkinter import DISABLED

from base.jsonstore import GhStorage
from basegui.application import GhApp
from basegui.simplepanel import GhSimplePanel
from launcher.gui.strings import Strings


class GameSession(GhSimplePanel):

    def __init__(self, parent, app, title_mode=False):
        super().__init__(parent)
        self.app = app
        self.session = None
        self.info = None
        self.selected = False
        self.title_mode = title_mode

        if not title_mode:
            self.ui_selection_check = GhApp.createCheckbox(self.content, 0, 0, self.applySelection)
            self.ui_selection_check.widget.grid_remove()
        else:
            self.ui_selection_check = GhApp.createCheckbox(self.content, 0, 0, self.applySelection)

        self.ui_mapping_entry = GhApp.createEntry(self.content, 0, 1, 20, "")
        self.ui_mapping_entry.widget.grid_remove()
        self.ui_mapping_entry.variable.set('PARENT')
        self.ui_date_label = GhApp.createLabel(self.content, 0, 2, width=15, anchor="center", justify='center')
        if title_mode:
            self.ui_date_label.variable.set(Strings.LAST_LAUNCH)
        self.ui_total_label = GhApp.createLabel(self.content, 0, 3, width=15, anchor="center", justify='center')
        if title_mode:
            self.ui_total_label.variable.set(Strings.TOTAL_DURATION)
        self.ui_last_label = GhApp.createLabel(self.content, 0, 4, width=15, anchor="center", justify='center')
        if title_mode:
            self.ui_last_label.variable.set(Strings.LAST_DURATION)
        self.ui_name_label = GhApp.createLabel(self.content, 0, 5)
        if title_mode:
            self.ui_name_label.variable.set(Strings.GAME_NAME)
        GhApp.createLabel(self.content, 0, 6, "", width=2)

    @staticmethod
    def setOptionalDateInfo(ui_label, info, info_name):
        val = GhStorage.getValue(info, info_name)
        if val is not None:
            ui_label.set(str(datetime.fromtimestamp(int(float(val)))))
        else:
            ui_label.set("-")

    @staticmethod
    def setOptionalDurationInfo(ui_label, info, info_name):
        val = int(float(GhStorage.getValue(info, info_name)))
        if val is not None:
            if val < 60:
                ui_label.set("{}s".format(str(val)))
            elif val < 3600:
                minute = int(val/60)
                second = int(val - (minute * 60))
                ui_label.set("{}m {}s".format(str(minute),str(second)))
            else:
                hour = int(val / 3600)
                minute = int((val - ( hour * 3600 )) / 60)
                ui_label.set("{}h{}m".format(str(val / 3600), str(minute)))
        else:
            ui_label.set("-")

    def set(self, session=None, info=None):
        self.session = session
        self.info = info
        if self.session is None:
            self.ui_date_label.variable.set("")
            self.ui_total_label.variable.set("")
            self.ui_last_label.variable.set("")
            self.ui_name_label.variable.set("")
            self.ui_selection_check.widget.grid_remove()
        else:
            self.ui_selection_check.widget.grid()
            GameSession.setOptionalDateInfo(self.ui_date_label.variable, info, 'last_session')
            GameSession.setOptionalDurationInfo(self.ui_total_label.variable, info, 'duration')
            GameSession.setOptionalDurationInfo(self.ui_last_label.variable, info, 'last_duration')
            self.ui_name_label.variable.set(self.session.getName())

    def getName(self):
        if self.session is None:
            return "-"
        else:
            return self.session.getName()

    def applySelection(self):
        self.selected = self.ui_selection_check.variable.get() == 1
        self.app.notifyEntrySelectionUpdate(self.selected, self.title_mode)

    def setSelected(self, mode):
        self.selected = mode
        if mode:
            self.ui_selection_check.variable.set(1)
        else:
            self.ui_selection_check.variable.set(0)

    def enableMapping(self):
        self.ui_mapping_entry.widget.grid()
        self.ui_date_label.widget.grid_remove()
        self.ui_total_label.widget.grid_remove()
        self.ui_last_label.widget.grid_remove()
        name = self.session.getName()
        original_name = self.session.getOriginName()
        if name == original_name:
            self.ui_name_label.variable.set(name)
        else:
            self.ui_name_label.variable.set("{} ( real name : {} )".format( name, original_name ))

    def disableMapping(self):
        self.ui_mapping_entry.widget.grid_remove()
        self.ui_date_label.widget.grid()
        self.ui_total_label.widget.grid()
        self.ui_last_label.widget.grid()
        self.ui_name_label.variable.set(self.session.getName())

    @staticmethod
    def create(parent, app, row, col, title_mode=None):
        result = GameSession(parent, app, title_mode=title_mode)
        parent.grid(row=0, column=col)
        return result
