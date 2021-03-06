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

from tkinter import LEFT


class GhAppHandle:
    def __init__(self, variable, widget, debug_name=None):
        self.widget = widget
        self.variable = variable
        self.debug_name = debug_name

    def grid(self):
        self.widget.grid()

    def grid_remove(self):
        if self.debug_name is not None:
            print("removing {}".format(self.debug_name))
        self.widget.grid_remove()

    def set(self, val):
        self.variable.set(val)

    def get(self):
        return self.variable.get()

    def cget(self, val):
        return self.widget.cget(val)

    def setImage(self, image, compound=LEFT):
        self.widget.configure(image=image)
        self.widget.configure(compound=compound)

    def setValues(self, values):
        self.widget['values'] = values
