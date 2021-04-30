from tkinter import Menu


class AppMenu:

    def __init__(self, parent, app):
        self.app = app
        self.popup_menu = Menu(parent,
                               tearoff=0)

        self.popup_menu.add_command(label="about",
                                    command=self.app.applyAbout)

        self.popup_menu.add_separator()

        self.popup_menu.add_command(label="exit",
                                    command=self.app.applyExit)

    # display menu on right click
    def do_popup(self, x, y):
        try:
            self.popup_menu.tk_popup(x, y)
        finally:
            self.popup_menu.grab_release()

