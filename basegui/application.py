from tkinter import Tk, Frame, Label, StringVar, Button, Entry, Checkbutton, Radiobutton, IntVar


class GhAppSetup:
    bg_header = 'light blue'
    bg_content = 'light grey'
    height = 550
    width = 550
    # center top bottom
    vertical = 'center'
    # position (digit) or center left right
    horizontal = 'center'


class GhAppHandle:
    def __init__(self, variable, widget):
        self.widget = widget
        self.variable = variable


class GhApp:

    def __init__(self, title):
        self.title = title

        self.window = Tk()

        # Set initial position from setup
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        if GhAppSetup.horizontal == 'right':
            x = screen_width - GhAppSetup.width - 10
        elif GhAppSetup.horizontal == 'center':
            x = int((screen_width - GhAppSetup.width) / 2)
        elif GhAppSetup.horizontal == 'left':
            x = 0
        else:
            x = int(GhAppSetup.horizontal)

        if GhAppSetup.vertical == 'bottom':
            y = screen_height - GhAppSetup.height - 10
        elif GhAppSetup.vertical == 'center':
            y = int((screen_height - GhAppSetup.height) / 2)
        elif GhAppSetup.vertical == 'top':
            y = 0
        else:
            y = int(GhAppSetup.vertical)

        self.window.title(title)
        self.window.geometry('{}x{}+{}+{}'.format(GhAppSetup.width, GhAppSetup.height, x, y))

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Build app skeleton ( header / content / footer )
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
                    justify='left',
                    width=None):
        textvariable = None
        if text is None:
            textvariable = StringVar()
        label = Label(parent,
                      text=text, textvariable=textvariable,
                      bg=parent.cget('bg'), width=width,
                      anchor=anchor, justify=justify)
        label.grid(row=row, column=col, sticky=anchor)
        return GhAppHandle(textvariable, label)

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
        return GhAppHandle(textvariable, button)

    @staticmethod
    def createRadio(parent, row, col, command,
                    text=None,
                    anchor='w',
                    padx=5):
        radiovar = IntVar()
        radio = Radiobutton(parent, bg=parent.cget('bg'), text=text,
                            command=command, variable=radiovar,
                            onvalue=1,
                            anchor=anchor, padx=padx)
        radio.grid(row=row, column=col, sticky=anchor)
        return GhAppHandle(radiovar, radio)

    @staticmethod
    def createCheckbox(parent, row, col, command,
                       text=None,
                       anchor='w',
                       padx=5):
        checkvar = IntVar()
        check = Checkbutton(parent, bg=parent.cget('bg'), text=text,
                            command=command, variable=checkvar,
                            onvalue=1,
                            anchor=anchor, padx=padx)
        check.grid(row=row, column=col, sticky=anchor)
        return GhAppHandle(checkvar, check)

    @staticmethod
    def createEntry(parent, row, col, width, defaultvalue,
                    padx=5, command=None):
        entryvar = StringVar()
        entryvar.set(defaultvalue)
        entry = Entry(parent, textvariable=entryvar, width=width, validatecommand=command)
        entry.grid(row=row, column=col, padx=padx)
        return GhAppHandle(entryvar, entry)
