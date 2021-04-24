from tkinter import Tk, Frame


class GhAppSetup:
    bg_header = 'light blue'
    bg_content = 'light grey'
    height = 550
    width = 550


class GhApp:

    def __init__(self, title):
        self.title = title

        self.window = Tk()

        self.window.title(title)
        self.window.geometry('{}x{}'.format(GhAppSetup.width, GhAppSetup.height))

        self.header = Frame(self.window, bg=GhAppSetup.bg_header, pady=5, padx=20)
        self.content = Frame(self.window, bg=GhAppSetup.bg_content, padx=5, pady=5)
        self.status = Frame(self.window, bg=GhAppSetup.bg_header, pady=3, padx=5)

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.header.grid(row=0, sticky="ew")
        self.content.grid(row=1, sticky="nsew")
        self.status.grid(row=2, sticky="ew")

    def start(self):
        self.window.mainloop()
        print("{} closed".format(self.title))