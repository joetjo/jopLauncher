from datetime import datetime

from base.jsonstore import GhStorage
from basegui.application import GhApp
from basegui.columnpanel import GhColumnPanel
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

        row = 0
        col = 0

        col_panel = GhColumnPanel(self.content)
        main_panel = col_panel.left
        action_panel = col_panel.right

        if not title_mode:
            self.ui_selection_check = GhApp.createCheckbox(main_panel, row, col, self.applySelection)
            self.ui_selection_check.widget.grid_remove()
        else:
            self.ui_selection_check = GhApp.createCheckbox(main_panel, row, col, self.applySelection)

        col += 1

        self.ui_mapping_entry = GhApp.createEntry(main_panel, row, col, 20, "")
        self.ui_mapping_entry.widget.grid_remove()
        self.ui_mapping_entry.variable.set('PARENT')

        col += 1

        self.ui_date_label = GhApp.createLabel(main_panel, row, col, width=15, anchor="center", justify='center')
        if title_mode:
            self.ui_date_label.variable.set(Strings.LAST_LAUNCH)

        col += 1

        self.ui_total_label = GhApp.createLabel(main_panel, row, col, width=15, anchor="center", justify='center')
        if title_mode:
            self.ui_total_label.variable.set(Strings.TOTAL_DURATION)

        col += 1

        self.ui_last_label = GhApp.createLabel(main_panel, row, col, width=15, anchor="center", justify='center')
        if title_mode:
            self.ui_last_label.variable.set(Strings.LAST_DURATION)

        col += 1

        self.ui_name_label = GhApp.createLabel(main_panel, row, col)
        if title_mode:
            self.ui_name_label.variable.set(Strings.GAME_NAME)

        # Actions column
        GhApp.createLabel(action_panel, 0, 0, text="  ", anchor="e")
        self.ui_launch_button = GhApp.createButton(action_panel, 0, 1, self.launchGame, text=">", anchor="e")
        self.ui_launch_button.widget.grid_remove()

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
        self.ui_launch_button.widget.grid_remove()
        name = self.session.getName()
        original_name = self.session.getOriginName()
        if name == original_name:
            self.ui_name_label.variable.set(name)
        else:
            self.ui_name_label.variable.set("{} ( real name : {} )".format(name, original_name))

    def disableMapping(self):
        self.ui_mapping_entry.widget.grid_remove()
        self.ui_date_label.widget.grid()
        self.ui_total_label.widget.grid()
        self.ui_last_label.widget.grid()
        self.ui_launch_button.widget.grid()
        if self.session is not None:
            self.ui_name_label.variable.set(self.session.getName())

    @staticmethod
    def create(parent, app, row, col, title_mode=None):
        result = GameSession(parent, app, title_mode=title_mode)
        parent.grid(row=0, column=col)  # TODO FIX THIS ROW+0 ??????????????????
        return result

    # ACTIONS !
    def launchGame(self):
        pass
