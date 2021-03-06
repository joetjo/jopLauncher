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

from tkinter import Frame

from gridgui.gridbehaviour import GhGridBehaviour


class GhColumnPanel(GhGridBehaviour):

    def __init__(self, parent):
        super().__init__(0, 0)
        self.left = Frame(parent,  bg=parent.cget('bg'), padx=0, pady=0)
        self.right = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)
        self.action = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.left.grid(row=self.row(), column=self.col_next(), sticky="nsw")
        self.right.grid(row=self.row(), column=self.col_next(), sticky="nse")
        self.action.grid(row=self.row(), column=self.col_next(), sticky="nse")
