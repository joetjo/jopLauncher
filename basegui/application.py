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
        self.footer = Frame(self.window, bg=GhAppSetup.bg_header, pady=3, padx=5)

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.header.grid(sticky="ew")
        self.content.grid(row=1, sticky="nsew")
        self.footer.grid(row=2, sticky="ew")

    def start(self):
        self.window.mainloop()
        print("{} closed".format(self.title))


class GhColumnPanel:

    def __init__(self, parent):
        self.left = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)
        self.right = Frame(parent, bg=parent.cget('bg'), padx=0, pady=0)

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.left.grid(sticky="nsw")
        self.right.grid(row=0, column=1, sticky="nse")
