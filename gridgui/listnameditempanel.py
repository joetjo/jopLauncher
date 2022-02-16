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

from base.pair import Pair
from gridgui.application import GhApp
from gridgui.simplepanel import GhSimplePanel


class GhListNamedItemPanel(GhSimplePanel):
    """
    ui_names : list(Pair(GhHandle for label, GhHandle for button)
    """

    def __init__(self, parent, title, row=0, col=0, names=None, sticky="nsew",
                 border_color=None, border_width=0, command=None, on_close=None,
                 images=None, close_image=None, remove_image=None):
        super().__init__(parent, row=row, col=col, sticky=sticky, border_color=border_color, border_width=border_width)
        self.command = command
        self.on_close = on_close
        self.border_color = border_color
        self.title = None
        self.images = images
        self.close_image = close_image
        self.remove_image = remove_image
        self.ui_items = []
        if names is not None:
            self.set(title, names)

        self.close = None
        self.sep = None

    def set(self, title, names, action_mode=True):
        self.clear()
        self.row_col_reset(row=1)
        if names is not None:
            self.title = GhApp.createLabel(self.content, self.row_next(), self.col(), bg=self.border_color,
                                           text=title, colspan=2, width=20)
            for name in names:
                label = GhApp.createLabel(self.content, self.row(), self.col_next(), text=name)
                if self.images is not None:
                    try:
                        label.setImage(self.images[name])
                    except KeyError:
                        pass
                button = None
                if action_mode:
                    button = GhApp.createButton(self.content, self.row_next(), self.col_reset(0),
                                                text="x", anchor='s',
                                                command=lambda current_name=name: self.command(current_name))
                    if self.remove_image is not None:
                        button.setImage(self.remove_image)
                        button.set("")
                else:
                    self.row_next()
                    self.col_reset(0)
                self.ui_items.append(Pair(label, button))

        self.col_reset()
        if action_mode:
            self.sep = GhApp.createLabel(self.content, self.row_next(), self.col_reset(), colspan=2, width=20)
            self.close = GhApp.createButton(self.content, self.row_next(), self.col_reset(),
                                            anchor='s', text=" close ", command=self.on_close)
            if self.close_image is not None:
                self.close.setImage(self.close_image)

    def clear(self):
        if self.title is not None:
            self.title.widget.destroy()
        for item in self.ui_items:
            if item.one is not None:
                item.one.widget.destroy()
            if item.two is not None:
                item.two.widget.destroy()
        if self.close is not None:
            self.close.widget.destroy()
            self.sep.widget.destroy()
        self.ui_items = []

    def grid_remove(self):
        if self.title is not None:
            self.title.widget.grid_remove()
        for item in self.ui_items:
            if item.one is not None:
                item.one.widget.grid_remove()
            if item.two is not None:
                item.two.widget.grid_remove()
        if self.close is not None:
            self.close.widget.grid_remove()
            self.sep.widget.grid_remove()

    def grid(self):
        self.title.widget.grid()
        for item in self.ui_items:
            if item.one is not None:
                item.one.widget.grid()
            if item.two is not None:
                item.two.widget.grid()
        if self.close is not None:
            self.close.widget.grid()
            self.sep.widget.grid()
