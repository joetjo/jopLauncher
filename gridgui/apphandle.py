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
