from base.pair import Pair
from basegui.application import GhApp
from basegui.simplepanel import GhSimplePanel


class GhListNamedItemPanel(GhSimplePanel):
    """
    ui_names : list(Pair(GhHandle for label, GhHandle for button)
    """

    def __init__(self, parent, title, row=0, col=0, names=None, sticky="nsew",
                 border_color=None, border_width=0, command=None, on_close=None):
        super().__init__(parent, row, col, sticky, border_color=border_color, border_width=border_width)
        self.parent = self.content
        self.command = command
        self.title = GhApp.createLabel(self.parent, self.row_next(), self.col(), bg=border_color,
                                       text=title, colspan=2, width=20)
        self.ui_items = []
        if names is not None:
            self.set(names)
        self.close = GhApp.createButton(self.parent, self.row_next(), self.col_next(),
                                        anchor='s', text="close", command=on_close)

    def set(self, names):
        self.clear()
        self.row_col_reset(row=1)
        if names is not None:
            for name in names:
                self.ui_items \
                    .append(Pair(GhApp.createLabel(self.parent, self.row(), self.col_next(), text=name),
                                 GhApp.createButton(self.parent, self.row_next(), self.col_reset(0),
                                                    text="x",
                                                    command=lambda current_name=name: self.command(current_name))))

    def clear(self):
        for item in self.ui_items:
            if item.one is not None:
                item.one.widget.destroy()
            if item.two is not None:
                item.two.widget.destroy()

    def grid_remove(self):
        self.title.widget.grid_remove()
        self.close.widget.grid_remove()
        for item in self.ui_items:
            if item.one is not None:
                item.one.widget.grid_remove()
            if item.two is not None:
                item.two.widget.grid_remove()

    def grid(self):
        self.title.widget.grid()
        self.close.widget.grid()
        for item in self.ui_items:
            if item.one is not None:
                item.one.widget.grid()
            if item.two is not None:
                item.two.widget.grid()
