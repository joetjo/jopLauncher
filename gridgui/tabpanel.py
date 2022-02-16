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

from tkinter import ttk

from gridgui.gridbehaviour import GhGridBehaviour


class GhTab(GhGridBehaviour):
    # PRIVATE - Use GhTabPanel::addTab
    def __init__(self, parent, title):
        super().__init__(0, 0)
        self.tab = ttk.Frame(parent)
        parent.add(self.tab, text=title)

    def getContainer(self):
        return self.tab


class GhTabPanel:
    # Parent: Window or main container
    def __init__(self, parent):
        self.tabRoot = ttk.Notebook(parent)

    def addTab(self, title):
        tab = GhTab(self.tabRoot, title)
        return tab

    def pack(self):
        self.tabRoot.pack(expand=1, fill='both')

