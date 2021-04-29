from tkinter import Tk, Frame, Label, StringVar, Button, Entry, Checkbutton, Radiobutton, IntVar

from basegui.gridbehaviour import GhGridBehaviour


class GhAppSetup:
    bg_header = 'light blue'
    bg_content = 'light grey'
    height = 550
    min_height = 250
    width = 550
    min_width = 400
    # center top bottom
    vertical = 'center'
    # position (digit) or center left right
    horizontal = 'center'
    icon = None
    image_button = True
    # Must not be false if image_button is false
    image_text_button = True


class GhAppHandle:
    def __init__(self, variable, widget):
        self.widget = widget
        self.variable = variable


'''
Generic Application based on grid layout with header / content / footer
mandatory : title ( application window title )
With static method to create widget ( and make of common look and feel application )
'''


class GhApp(GhGridBehaviour):

    def __init__(self, title):
        super().__init__(0, 0)
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
        self.window.iconbitmap(GhAppSetup.icon)

        self.window.geometry('{}x{}+{}+{}'.format(GhAppSetup.width, GhAppSetup.height, x, y))
        self.window.minsize(GhAppSetup.min_width, GhAppSetup.min_height)

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
    def setupImage(widget, image, align):
        widget.config(image=image, compound=align)

    @staticmethod
    # if text is None, create a StringVar and return it
    def createLabel(parent, row, col,
                    text=None,
                    anchor='w',
                    justify='left',
                    colspan=1,
                    width=None):
        text_variable = None
        if text is None:
            text_variable = StringVar()
        label = Label(parent,
                      text=text, textvariable=text_variable,
                      bg=parent.cget('bg'), width=width,
                      anchor=anchor, justify=justify)
        if anchor == 'center':
            anchor = 'w'
        label.grid(row=row, column=col, sticky=anchor, columnspan=colspan)
        return GhAppHandle(text_variable, label)

    @staticmethod
    def createButton(parent, row, col,
                     command,
                     text,
                     anchor='w',
                     padx=5,
                     width=None,
                     image=None):
        text_variable = StringVar()

        button = Button(parent, command=command, textvariable=text_variable,
                        anchor=anchor, padx=padx, width=width)
        button.grid(row=row, column=col, sticky=anchor)

        if not GhAppSetup.image_button \
                or GhAppSetup.image_text_button \
                or image is None:
            text_variable.set(text)

        if GhAppSetup.image_button:
            GhApp.setupImage(button, image, "left")
        return GhAppHandle(text_variable, button)

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
