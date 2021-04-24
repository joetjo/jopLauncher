from datetime import datetime, timedelta

from basegui.application import GhApp
from basegui.simplepanel import GhSimplePanel


class GameSession(GhSimplePanel):

    def __init__(self, parent):
        super().__init__(parent)
        self.name = None
        self.info = None
        self.selected = False

        self.check = GhApp.createCheckbox(self.content, 0, 0, self.selection)
        self.check.widget.grid_remove()
        self.mapping = GhApp.createEntry(self.content, 0, 1, 20, "")
        self.mapping.widget.grid_remove()
        self.mapping.variable.set('PARENT')
        self.label = GhApp.createLabel(self.content, 0, 2).variable

    def set(self, name=None, info=None):
        self.name = name
        self.info = info
        if name is None:
            self.label.set("")
            self.check.widget.grid_remove()
        else:
            self.check.widget.grid()
            date = datetime.fromtimestamp(int(float(info['last_session'])))
            deltaTotal = timedelta(seconds=float(info['duration']))
            deltaLast = timedelta(seconds=float(info['last_duration']))
            self.label.set("{} | {} | {} | {}".format(date, deltaLast, deltaTotal, name))

    def selection(self):
        self.selected = self.check.variable.get() == 1

    def deselect(self):
        self.selected = False
        self.check.variable.set(0)

    def enableMapping(self):
        self.mapping.widget.grid()

    def disableMapping(self):
        self.mapping.widget.grid_remove()

    @staticmethod
    def create(parent, row, col):
        result = GameSession(parent)
        parent.grid(row=0, column=col)
        return result
