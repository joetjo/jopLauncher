from datetime import datetime, timedelta

from base.jsonstore import GhStorage
from basegui.application import GhApp
from basegui.simplepanel import GhSimplePanel


class GameSession(GhSimplePanel):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.name = None
        self.info = None
        self.selected = False

        self.ui_selection_check = GhApp.createCheckbox(self.content, 0, 0, self.applySelection)
        self.ui_selection_check.widget.grid_remove()
        self.ui_mapping_entry = GhApp.createEntry(self.content, 0, 1, 20, "")
        self.ui_mapping_entry.widget.grid_remove()
        self.ui_mapping_entry.variable.set('PARENT')
        self.ui_date_label = GhApp.createLabel(self.content, 0, 2, width=15)
        self.ui_total_label = GhApp.createLabel(self.content, 0, 3, width=15)
        self.ui_last_label = GhApp.createLabel(self.content, 0, 4, width=15)
        self.ui_name_label = GhApp.createLabel(self.content, 0, 5)

    @staticmethod
    def setOptionalInfo(ui_label, info, info_name):
        val = GhStorage.getValue(info, info_name)
        if val is not None:
            ui_label.set(str(datetime.fromtimestamp(int(float(val)))))
        else:
            ui_label.set("-")

    def set(self, name=None, info=None):
        self.name = name
        self.info = info
        if name is None:
            self.ui_date_label.variable.set("")
            self.ui_total_label.variable.set("")
            self.ui_last_label.variable.set("")
            self.ui_name_label.variable.set("")
            self.ui_selection_check.widget.grid_remove()
        else:
            self.ui_selection_check.widget.grid()
            GameSession.setOptionalInfo(self.ui_date_label.variable, info, 'last_session')
            GameSession.setOptionalInfo(self.ui_total_label.variable, info, 'duration')
            GameSession.setOptionalInfo(self.ui_last_label.variable, info, 'last_duration')
            self.ui_name_label.variable.set(name)

    def applySelection(self):
        self.selected = self.ui_selection_check.variable.get() == 1
        self.app.notifyEntrySelectionUpdate()

    def deselect(self):
        self.selected = False
        self.ui_selection_check.variable.set(0)

    def enableMapping(self):
        self.ui_mapping_entry.widget.grid()
        self.ui_date_label.widget.grid_remove()
        self.ui_total_label.widget.grid_remove()
        self.ui_last_label.widget.grid_remove()

    def disableMapping(self):
        self.ui_mapping_entry.widget.grid_remove()
        self.ui_date_label.widget.grid()
        self.ui_total_label.widget.grid()
        self.ui_last_label.widget.grid()


    @staticmethod
    def create(parent, app, row, col):
        result = GameSession(parent, app)
        parent.grid(row=0, column=col)
        return result
