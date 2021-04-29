from basegui.application import GhApp
from basegui.simplepanel import GhSimplePanel
from launcher.gui.strings import Strings


# Global actions panel to use when a game is selected
class GameActionPanel(GhSimplePanel):

    def __init__(self, parent, app, row=0, col=0, sticky="nsew"):
        super().__init__(parent, row, col, sticky=sticky)

        self.app = app

        self.ui_ignore_button = GhApp.createButton(parent, self.row(), self.col_next(), app.applyIgnore, Strings.IGNORE_ACTION)
        self.ui_remove_button = GhApp.createButton(parent, self.row(), self.col_next(), app.applyRemove, Strings.REMOVE_ACTION)
        self.ui_mapping_button = GhApp.createButton(parent, self.row(), self.col_next(), app.applyMapping, Strings.MAPPING_ACTION)
        self.ui_cancel_button = GhApp.createButton(parent, self.row(), self.col_next(), app.applyCancelMapping, Strings.MAPPING_CANCEL_ACTION)

    # No game selected mode
    def grid_remove(self):
        self.ui_cancel_button.widget.grid_remove()
        self.ui_ignore_button.widget.grid_remove()
        self.ui_remove_button.widget.grid_remove()
        self.ui_mapping_button.widget.grid_remove()

    # Game selected mode
    def grid(self):
        self.ui_ignore_button.widget.grid()
        self.ui_remove_button.widget.grid()
        self.ui_mapping_button.widget.grid()
        self.ui_cancel_button.widget.grid_remove()
        self.ui_mapping_button.variable.set(Strings.MAPPING_ACTION)

    # Game selected mode + mapping in progress
    def enableMapping(self):
        self.ui_mapping_button.variable.set(Strings.MAPPING_APPLY_ACTION)
        self.ui_cancel_button.widget.grid()

    # Just cancel mapping mode without impact on other button
    def disableMapping(self):
        self.ui_mapping_button.variable.set(Strings.MAPPING_ACTION)
        self.ui_cancel_button.widget.grid_remove()

    def isMappingEnabled(self):
        return self.ui_mapping_button.variable.get() == Strings.MAPPING_APPLY_ACTION
