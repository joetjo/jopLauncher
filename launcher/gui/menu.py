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

from JopLauncherConstant import JopLauncher, JopSETUP
from base.fileutil import GhFileUtil
from gridgui.appmenu import GhAppMenu
from launcher.gui.strings import Strings


class PlatformLauncher:

    def __init__(self, menu, gui, entry, command):
        self.gui = gui
        self.entry = entry
        self.command = command
        menu.add("{} {}".format(Strings.LAUNCH_PLATFORM_MENU, entry), self.apply)

    def apply(self):
        self.gui.applyLaunchPlatform(self.entry, self.command)


class MainMenu(GhAppMenu):

    def __init__(self, parent, app, gui):
        super().__init__(parent, app)

        self.add(Strings.MENU_EXCLUDED, gui.applyShowExcluded)
        self.add(Strings.MENU_LAUNCHER, gui.applyShowLauncher)
        self.addSep()
        for key in JopLauncher.GAME_PLATFORMS:
            entry = JopLauncher.GAME_PLATFORMS[key]
            cmd = JopSETUP.get(entry)
            if GhFileUtil.fileExist(cmd[0]):
                PlatformLauncher(self, gui, entry, cmd)
        self.addSep()
        self.add(Strings.MENU_COMP_APP, gui.applyLaunchCompApp)
        self.add(Strings.MENU_MARKDOWN_REPORT, gui.updateMarkdownReport)
        self.add(Strings.MENU_ICONFX_APP, gui.applyLaunchIconExtract)
        self.addSep()
        self.add(Strings.EXIT, gui.applyExit)
