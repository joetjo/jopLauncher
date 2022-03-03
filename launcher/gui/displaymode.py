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

from base.fileutil import GhFileUtil
from launcher.gui.strings import Strings
from launcher.log import Log


class Filter:

    def __init__(self, attribute, value, operatorIsEqual):
        self.attribute = attribute
        self.value = value
        self.operatorIsEqual = operatorIsEqual


class DisplayMode:
    """Keep track of display mode used by ProcGUI

    - searchMode : True is search display is in progress / or this is the last sessions display
    - display_mode_string : previous value for the search mode string visible in GUI
    - ui_... component widget (
    """

    def __init__(self, app):
        self.app = app

        # PREVIOUS or SEARCH
        self.display_mode_string = Strings.PREVIOUS
        # DISPLAY MODE : search or last_session
        self.search_mode = False
        # RESULT FILTER: show or not show : only installed game
        self.installed_mode = True
        # RESULT FILTER: show or not show : game that match the extended filter
        self.extended_mode = False
        self.filters = []
        # OPTIONAL DISPLAY
        self.excluded_mode = False
        self.launcher_mode = False
        self.platform_mode = True

    def enableLastSessionMode(self):
        self.search_mode = False
        self.display_mode_string = Strings.PREVIOUS
        self.app.ui_search_entry.set("")
        self.app.ui_prev_session_label.set(self.display_mode_string)
        self.app.ui_search_reset_button.grid_remove()

    def enableSearchMode(self):
        self.search_mode = True
        self.app.ui_prev_session_label.set(Strings.SEARCHING)
        self.app.ui_search_reset_button.grid()

    def searchResult(self, result):
        self.display_mode_string = result
        self.app.ui_prev_session_label.set(self.display_mode_string)

    def filterMode(self, installed_mode, extended_mode):
        self.installed_mode = installed_mode
        self.extended_mode = extended_mode

        # reload in current mode
        self.refreshSessions()

    def editExtendedFilter(self):
        Log.debug("UI: editExtendedFilter")
        self.app.ui_extended_filter_toolbar.grid()
        self.app.ui_extended_filter_toolbar.setFilters(self.filters)

    def isSearchInProgress(self):
        return self.search_mode

    # check if game from session map the current filter mode
    def isVisible(self, session):
        installCheck = (self.installed_mode and GhFileUtil.fileExist(session.getPath())) or not self.installed_mode
        extendCheck = True
        if self.extended_mode:
            for f in self.filters:
                value = self.getValueFor(f.attribute, session)
                if f.operatorIsEqual:
                    extendCheck = extendCheck and value == f.value
                else:
                    extendCheck = extendCheck and not value == f.value
        return installCheck and extendCheck

    @staticmethod
    def getValueFor(attribute, session):
        if attribute == "Status":
            return session.getStatus()
        if attribute == "Type":
            return session.getType()
        if attribute == "Note":
            return session.getNote()
        Log.info("Warning Extended filter : invalid attribute type {}".format(attribute))
        return ""

    def showExcluded(self):
        self.excluded_mode = True
        self.platform_mode = False
        self.launcher_mode = False
        self.app.ui_options.set(Strings.EXCLUDED_GAME, self.app.procMgr.game_ignored)

    def showLauncher(self):
        self.excluded_mode = False
        self.platform_mode = False
        self.launcher_mode = True
        self.app.ui_options.set(Strings.LAUNCHERS, self.app.procMgr.game_launchers)

    def showPlatforms(self):
        self.closeExtended()

    def closeExtended(self):
        if self.app.ui_options is not None:
            self.excluded_mode = False
            self.launcher_mode = False
            self.platform_mode = True
            self.app.ui_options.set(Strings.PLATFORMS, self.app.procMgr.platforms, action_mode=False)

    # refresh display according to current mode
    def refreshSessions(self):
        if self.search_mode:
            Log.debug("UI: refresh search result")
            self.app.applySearch()
        else:
            Log.debug("UI: refresh last session list")
            self.app.reloadLastSessions()

    def refreshExtended(self):
        if self.excluded_mode:
            self.showExcluded()
        elif self.launcher_mode:
            self.showLauncher()
        else:
            self.showPlatforms()

    def applyExtendedFilter(self, filters):
        Log.info("Applying filter setup {}".format(len(filters)))
        self.filters = filters
