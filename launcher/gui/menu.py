from gridgui.appmenu import GhAppMenu
from launcher.gui.strings import Strings


class MainMenu(GhAppMenu):

    def __init__(self, parent, app, gui):
        super().__init__(parent, app)

        self.add(Strings.MENU_EXCLUDED, gui.applyShowExcluded)
        self.add(Strings.MENU_LAUNCHER, gui.applyShowLauncher)
        self.addSep()
        self.add(Strings.MENU_COMP_APP, gui.applyLaunchCompApp)
        self.addSep()
        self.add(Strings.EXIT, gui.applyExit)
