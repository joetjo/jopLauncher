# Copyright 2022 joetjo https://github.com/joetjo/MarkdownHelper
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
from launcher.gui.displaymode import Filter
from launcher.gui.strings import Strings

# Extender filter editor
from launcher.log import Log

COMBO_WIDTH = 15
ATTRIBUTES_SUPPORTED = ["Status", "Type", "Note"]
ATTRIBUTE_STATUS = 0
ATTRIBUTE_TYPE = 1
ATTRIBUTE_NOTE = 2
OPERATOR_EQUAL = "="
OPERATOR_DIFF = "!="
OPERATOR_SUPPORTED = [OPERATOR_EQUAL, OPERATOR_DIFF]


class FilerLinePanel(GhSimplePanel):

    def __init__(self, parent, filterPanel, row, col, sticky="nsew"):
        super().__init__(parent, row, col, colspan=6, sticky=sticky)

        self.content = parent
        self.filterRow = row
        self.filterCol = col
        self.parent = parent
        self.filterPanel = filterPanel
        self.ui_attribute_selector = GhApp.createCombobox(parent, row, col,
                                                          self.applyTypeSelection, ATTRIBUTES_SUPPORTED,
                                                          width=COMBO_WIDTH)
        self.ui_attribute_selector.set(ATTRIBUTES_SUPPORTED[0])
        self.ui_operator_selector = GhApp.createCombobox(parent, row, col + 1,
                                                         self.applyOperatorSelection, OPERATOR_SUPPORTED,
                                                         width=2)
        self.ui_operator_selector.set(OPERATOR_SUPPORTED[0])
        self.ui_value_selector = GhApp.createCombobox(parent, row, col + 2,
                                                      self.applyValueSelection, "",
                                                      width=COMBO_WIDTH)
        self.applyTypeSelection(self.ui_attribute_selector.get())
        self.ui_del_button = GhApp.createButton(parent, row, col + 3,
                                                self.applyDel, Strings.DEL_FILTER_ACTION,
                                                image=self.filterPanel.app.icons.REMOVE,
                                                text_visible=False, anchor="w")
        # A Unique + button on last line
        self.addLastLineButtons()

    def addLastLineButtons(self):
        self.filterPanel.ui_add_button = GhApp.createButton(self.parent, self.filterRow, self.filterCol + 4,
                                                            self.filterPanel.applyAdd, Strings.ADD_FILTER_ACTION,
                                                            image=self.filterPanel.app.icons.PLUS,
                                                            text_visible=False, anchor="w")
        self.filterPanel.ui_ok_button = GhApp.createButton(self.parent, self.filterRow, self.filterCol + 5,
                                                           self.filterPanel.applyOK, Strings.APPLY_FILTER_ACTION,
                                                           text_visible=True, anchor="w")

    def grid_remove(self):
        self.ui_attribute_selector.grid_remove()
        self.ui_operator_selector.grid_remove()
        self.ui_value_selector.grid_remove()
        self.ui_del_button.grid_remove()

    def grid(self):
        self.ui_attribute_selector.grid()
        self.ui_operator_selector.grid()
        self.ui_value_selector.grid()
        self.ui_del_button.grid()

    def applyDel(self):
        self.filterPanel.applyDel(self)

    def applyTypeSelection(self, info):
        self.ui_value_selector.setValues(self.filterPanel.getPossibleValues(self.ui_attribute_selector.get()))
        self.ui_value_selector.set("")

    def applyOperatorSelection(self, info):
        self.filterPanel.saveFilters()

    def applyValueSelection(self, info):
        self.filterPanel.saveFilters()


class ExtenderFilterPanel(GhSimplePanel):

    def __init__(self, parent, app, row=0, col=0, sticky="nsew"):
        super().__init__(parent, row, col, colspan=6, sticky=sticky)

        self.filterColumn = 4
        self.filterRow = row

        self.app = app
        self.filters = []

        self.ui_title = GhApp.createLabel(parent, self.row(), self.col_next(), colspan=6)
        self.ui_add_button = None
        self.ui_ok_button = None
        self.editMode = False
        self.row_next()

    def grid_remove(self):
        if self.ui_add_button is not None:
            self.ui_add_button.grid_remove()
            self.ui_ok_button.grid_remove()

    def grid(self):
        if self.ui_add_button is not None:
            self.ui_add_button.grid()
            self.ui_ok_button.grid()

    def enableEdit(self):
        self.editMode = True
        self.grid()
        self.hideFilterLabel()

    def disableEdit(self):
        self.editMode = False
        for filterPanel in self.filters:
            filterPanel.grid_remove()
        if len(self.filters) == 0:
            self.ui_title.grid_remove()
        else:
            message = ""
            for f in self.filters:
                message = "{} {} {} {} |".format(message,
                                                 f.ui_attribute_selector.get(),
                                                 f.ui_operator_selector.get(),
                                                 f.ui_value_selector.get())
            self.ui_title.set(message)
            self.showFilterLabel()
        self.grid_remove()

    def hideFilterLabel(self):
        self.ui_title.grid_remove()

    def showFilterLabel(self):
        self.ui_title.grid()

    def setFilters(self, filters):
        self.filters = []
        self.row_reset(self.filterRow)

        for f in filters:
            filterPanel = self.applyAdd()
            filterPanel.ui_attribute_selector.set(f.attribute)
            if f.operatorIsEqual:
                filterPanel.ui_operator_selector.set(OPERATOR_EQUAL)
            else:
                filterPanel.ui_operator_selector.set(OPERATOR_DIFF)
            filterPanel.applyTypeSelection(filterPanel.ui_attribute_selector.get())
            filterPanel.ui_value_selector.set(f.value)

        if len(self.filters) == 0:
            self.applyAdd()

    def getLastFilterPanel(self):
        filterCount = len(self.filters)
        if filterCount == 0:
            return None
        else:
            return self.filters[filterCount - 1]

    def applyAdd(self):
        Log.info("Adding filter {} {}".format(self.row(), self.filterColumn))
        self.grid_remove()
        filterPanel = FilerLinePanel(self.content, self, self.row_next(), self.filterColumn)
        self.filters.append(filterPanel)
        return filterPanel

    def applyDel(self, filterPanel):
        # Last line need a specific processing - last line detection
        lastFilter = self.getLastFilterPanel()
        lastLine = False
        if lastFilter is not None and lastFilter == filterPanel:
            lastLine = True
        # Removing the requested filter
        self.filters.remove(filterPanel)
        filterPanel.grid_remove()
        Log.info("Filter line removed --> remaining filter: {}".format(len(self.filters)))
        # Processing the last line case if needed
        if lastLine:
            lastFilter = self.getLastFilterPanel()
            if lastFilter is not None:
                self.grid_remove()
                lastFilter.addLastLineButtons()

    def saveFilters(self):
        filters = []
        for filterPanel in self.filters:
            filters.append(Filter(filterPanel.ui_attribute_selector.get(),
                                  filterPanel.ui_value_selector.get(),
                                  filterPanel.ui_operator_selector.get() is OPERATOR_EQUAL))
        self.app.saveFilterSetup(filters)

    def applyOK(self):
        self.saveFilters()
        self.disableEdit()
        self.app.applyFilterSetup(self.filters)

    def getPossibleValues(self, attribute):
        result = [""]
        values = None
        if attribute == ATTRIBUTES_SUPPORTED[ATTRIBUTE_TYPE]:
            values = self.app.procMgr.getPossibleTypes()
        if attribute == ATTRIBUTES_SUPPORTED[ATTRIBUTE_STATUS]:
            values = self.app.procMgr.getPossibleStatuses()
        if attribute == ATTRIBUTES_SUPPORTED[ATTRIBUTE_NOTE]:
            values = self.app.procMgr.getPossibleNotes()

        if len(values) == 0:
            Log.info("WARNING: no value for attribute {}".format(attribute))
        else:
            for value in values:
                result.append(value)

        return result
