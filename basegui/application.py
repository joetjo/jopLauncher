from tkinter import Tk, Frame, Label, StringVar, Button, Entry


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

    @staticmethod
    # if text is None, create a StringVar and return it
    def createLabel(parent, row, col,
                    text=None,
                    anchor='w',
                    justify='left'):
        textvariable = None
        if text is None:
            textvariable = StringVar()
        label = Label(parent,
                      text=text, textvariable=textvariable,
                      bg=parent.cget('bg'),
                      anchor=anchor, justify=justify)
        label.grid(row=row, column=col, sticky=anchor)
        if textvariable is not None:
            return textvariable
        return label

    @staticmethod
    def createButton(parent, row, col,
                     command,
                     text,
                     anchor='w',
                     padx=5):
        textvariable = StringVar()
        textvariable.set(text)
        button = Button(parent, command=command, textvariable=textvariable,
                        anchor=anchor, padx=padx)
        button.grid(row=row, column=col, sticky=anchor)
        if textvariable is not None:
            return textvariable
        return button

    @staticmethod
    def createEntry(parent, row, col, width, defaultvalue,
                    padx=5):
        entryvar = StringVar()
        entryvar.set(defaultvalue)
        entry = Entry(parent, textvariable=entryvar, width=width)
        entry.grid(row=row, column=col, padx=padx)
        return entryvar
