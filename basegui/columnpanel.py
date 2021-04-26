from tkinter import Frame


class GhColumnPanel:

    def __init__(self, parent):
        self.left = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)
        self.right = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)
        self.action = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.left.grid(row=0, column=0, sticky="nsw")
        self.right.grid(row=0, column=1, sticky="nse")
        self.action.grid(row=0, column=2, sticky="nse")
