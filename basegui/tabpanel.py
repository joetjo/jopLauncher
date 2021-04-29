from tkinter import ttk

from basegui.gridbehaviour import GhGridBehaviour


class GhTab(GhGridBehaviour):
    # PRIVATE - Use GhTabPanel::addTab
    def __init__(self, parent, title):
        super().__init__(0, 0)
        self.tab = ttk.Frame(parent)
        parent.add(self.tab, text=title)

    def getContainer(self):
        return self.tab


class GhTabPanel:
    # Parent: Window or main container
    def __init__(self, parent):
        self.tabRoot = ttk.Notebook(parent)

    def addTab(self, title):
        tab = GhTab(self.tabRoot, title)
        return tab

    def pack(self):
        self.tabRoot.pack(expand=1, fill='both')

