from tkinter import Frame

from basegui.gridbehaviour import GhGridBehaviour


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
