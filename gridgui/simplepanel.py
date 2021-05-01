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
