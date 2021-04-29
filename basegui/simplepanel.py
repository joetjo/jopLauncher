from tkinter import Frame

from basegui.gridbehaviour import GhGridBehaviour


class GhSimplePanel(GhGridBehaviour):

    def __init__(self, parent, row=0, col=0, sticky="nsew"):
        super().__init__(row, col)
        self.content = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)
        self.content.grid(row=row, column=col, sticky=sticky)

    def grid_remove(self):
        self.content.grid_remove()

    def grid(self):
        self.content.grid()
