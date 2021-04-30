from tkinter import Menu


class GhAppMenu:

    def __init__(self, parent, app):
        self.app = app
        self.popup_menu = Menu(parent,
                               tearoff=0)

    def add(self, label, command):
        self.popup_menu.add_command(label=label,
                                    command=command)

    def addSep(self):
        self.popup_menu.add_separator()

    def pop(self):
        try:
            self.popup_menu.tk_popup(self.app.getMouseX(), self.app.getMouseY())
        finally:
            self.popup_menu.grab_release()
