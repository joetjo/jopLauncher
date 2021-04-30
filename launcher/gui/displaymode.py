from base.fileutil import GhFileUtil
from launcher.gui.strings import Strings


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
        # RESULT FILTER: show or not show only installed game
        self.installed_mode = False
        # OPTIONAL DISPLAY
        self.excluded_mode = False
        self.launcher_mode = False

    def enableLastSessionMode(self):
        self.search_mode = False
        self.display_mode_string = Strings.PREVIOUS
        self.app.ui_search_entry.variable.set("")
        self.app.ui_prev_session_label.variable.set(self.display_mode_string)
        self.app.ui_search_reset_button.widget.grid_remove()

    def enableSearchMode(self):
        self.search_mode = True
        self.app.ui_prev_session_label.variable.set(Strings.SEARCHING)
        self.app.ui_search_reset_button.widget.grid()

    def searchResult(self, result):
        self.display_mode_string = result
        self.app.ui_prev_session_label.variable.set(self.display_mode_string)

    def filterMode(self, installed_mode):
        self.installed_mode = installed_mode
        # reload in current mode
        self.refreshSessions()

    def isSearchInProgress(self):
        return self.search_mode

    # check if game from session map the current filter mode
    def isVisible(self, session):
        return (self.installed_mode and GhFileUtil.fileExist(session.getPath())) or not self.installed_mode

    def showExcluded(self):
        self.app.ui_options.grid()
        self.excluded_mode = True
        self.launcher_mode = False
        self.app.ui_options.set(self.procMgr.game_ignored)

    def showLauncher(self):
        self.app.ui_options.grid()
        self.excluded_mode = False
        self.launcher_mode = True
        self.app.ui_options.set(self.procMgr.game_ignored)

    def closeExtended(self):
        self.excluded_mode = False
        self.launcher_mode = False
        self.app.ui_options.grid_remove()

    # refresh display according to current mode
    def refreshSessions(self):
        if self.search_mode:
            print("UI: refresh search result")
            self.app.applySearch()
        else:
            print("UI: refresh last session list")
            self.app.reloadLastSessions()
