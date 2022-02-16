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


class GhSimplePanel(GhGridBehaviour):

    def __init__(self, parent, row=0, col=0, colspan=1, sticky="nsew",
                 border_color=None, border_width=0):
        super().__init__(row, col)

        if border_color is None:
            content_parent = parent
        else:
            content_parent = Frame(parent, bg=border_color, padx=border_width, pady=border_width)
            content_parent.grid(row=row, column=col, columnspan=colspan, sticky=sticky)

        self.content = Frame(content_parent, bg=parent.cget('bg'), padx=0, pady=0)
        self.content.grid(row=row, column=col, columnspan=colspan, sticky=sticky)

    """
            highlightbackground="black" and highlightthickness=1
            

    """

    def grid_remove(self):
        self.content.grid_remove()

    def grid(self):
        self.content.grid()
