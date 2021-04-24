from tkinter import Frame


class GhSimplePanel:

    def __init__(self, parent):
        self.content = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)
        self.content.grid(sticky="nswe")

