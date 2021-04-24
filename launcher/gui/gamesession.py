from datetime import datetime, timedelta

from basegui.application import GhApp
from basegui.simplepanel import GhSimplePanel


class GameSession(GhSimplePanel):

    def __init__(self, parent):
        super().__init__(parent)
        self.name = None
        self.info = None

        self.label = GhApp.createLabel(self.content, 0, 0)

    def set(self, name=None, info=None):
        self.name = name
        self.info = info
        if name is None:
            self.label.set("")
        else:
            date = datetime.fromtimestamp(int(float(info['last_session'])))
            deltaTotal = timedelta(seconds=float(info['duration']))
            deltaLast = timedelta(seconds=float(info['last_duration']))
            self.label.set("{} | {} | {} | {}".format(date, deltaLast, deltaTotal, name))


    @staticmethod
    def create(parent, row, col):
        result = GameSession(parent)
        parent.grid(row=0, column=col)
        return result
