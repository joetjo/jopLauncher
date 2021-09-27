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

from gridgui.application import GhApp
from gridgui.simplepanel import GhSimplePanel
from launcher.gui.strings import Strings


# Global actions panel to use when a game is selected
class GameActionPanel(GhSimplePanel):

    def __init__(self, parent, app, row=0, col=0, sticky="nsew"):
        super().__init__(parent, row, col, sticky=sticky)

        self.app = app

        self.ui_edit_button = GhApp.createButton(parent, self.row(), self.col_next(),
                                                 app.applyEdit, Strings.EDIT_ACTION, image=self.app.icons.EDIT,
                                                 text_visible=True)
        self.ui_edit_end_button = GhApp.createButton(parent, self.row(), self.col_next(),
                                                     app.applyCancelEdit, Strings.EDIT_CANCEL_ACTION,
                                                     image=self.app.icons.CANCEL_EDIT, text_visible=True)
        self.ui_ignore_button = GhApp.createButton(parent, self.row(), self.col_next(),
                                                   app.applyIgnore, Strings.IGNORE_ACTION,
                                                   image=self.app.icons.NA, text_visible=True)
        self.ui_remove_button = GhApp.createButton(parent, self.row(), self.col_next(),
                                                   app.applyRemove, Strings.REMOVE_ACTION,
                                                   image=self.app.icons.REMOVE, text_visible=True)
        self.ui_mapping_button = GhApp.createButton(parent, self.row(), self.col_next(),
                                                    app.applyMapping, Strings.MAPPING_ACTION,
                                                    image=self.app.icons.SWITCH, text_visible=True)
        self.ui_cancel_button = GhApp.createButton(parent, self.row(), self.col_next(),
                                                   app.applyCancelMapping, Strings.MAPPING_CANCEL_ACTION,
                                                   image=self.app.icons.ESCAPE, text_visible=True)

    # No game selected mode
    def grid_remove(self):
        self.ui_edit_button.grid_remove()
        self.ui_edit_end_button.grid_remove()
        self.ui_cancel_button.grid_remove()
        self.ui_ignore_button.grid_remove()
        self.ui_remove_button.grid_remove()
        self.ui_mapping_button.grid_remove()

    # Game selected mode
    def grid(self):
        self.ui_edit_button.grid()
        self.ui_ignore_button.grid()
        self.ui_remove_button.grid()
        self.ui_mapping_button.grid()
        self.ui_cancel_button.grid_remove()
        self.ui_edit_end_button.grid_remove()
        self.ui_mapping_button.set(Strings.MAPPING_ACTION)
        self.ui_edit_button.set(Strings.EDIT_ACTION)

    # Game selected mode + mapping in progress
    def enableMapping(self):
        self.ui_mapping_button.set(Strings.MAPPING_APPLY_ACTION)
        self.ui_cancel_button.grid()

    # Just cancel mapping mode without impact on other button
    def disableMapping(self):
        self.ui_mapping_button.set(Strings.MAPPING_ACTION)
        self.ui_cancel_button.grid_remove()

    def isMappingEnabled(self):
        return self.ui_mapping_button.get() == Strings.MAPPING_APPLY_ACTION

    # Game selected mode + mapping in progress
    def enableEdit(self):
        self.ui_edit_button.set(Strings.EDIT_APPLY_ACTION)
        self.ui_edit_end_button.grid()

    # Just cancel mapping mode without impact on other button
    def disableEdit(self):
        self.ui_edit_button.set(Strings.EDIT_ACTION)
        self.ui_edit_end_button.grid_remove()

    def isEditEnabled(self):
        return self.ui_edit_button.get() == Strings.EDIT_APPLY_ACTION
