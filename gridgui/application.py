from tkinter import Tk, Frame, Label, StringVar, Button, Entry, Checkbutton, Radiobutton, IntVar
from tkinter.ttk import Combobox

from gridgui.apphandle import GhAppHandle
from gridgui.gridbehaviour import GhGridBehaviour


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


'''
Generic Application based on grid layout with header / content / footer
mandatory : title ( application window title )
With static method to create widget ( and make of common look and feel application )
'''


class GhApp(GhGridBehaviour):

    def __init__(self, title, exit_command):
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
        self.window.protocol("WM_DELETE_WINDOW", exit_command)

        # Build app skeleton ( header / content / footer )
        self.header = Frame(self.window, bg=GhAppSetup.bg_header, pady=5, padx=5)
        self.content = Frame(self.window, bg=GhAppSetup.bg_content, padx=0, pady=0)
        self.footer = Frame(self.window, bg=GhAppSetup.bg_header, pady=3, padx=5)

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.header.grid(sticky="ew")
        self.content.grid(row=1, sticky="nsew")
        self.footer.grid(row=2, sticky="ew")

    def getMouseX(self):
        return self.window.winfo_pointerx()  # - self.window.winfo_rootx()

    def getMouseY(self):
        return self.window.winfo_pointery()  # - self.window.winfo_rooty()

    def start(self):
        self.window.mainloop()
        print("{} closed".format(self.title))

    def close(self):
        self.window.quit()

    @staticmethod
    def setupImage(widget, image, align):
        widget.config(image=image, compound=align)

    @staticmethod
    # if text is None, create a StringVar and return it
    def createLabel(parent, row, col,
                    text=None,
                    anchor='w',
                    justify='left',
                    image=None,
                    colspan=1,
                    width=None,
                    bg=None,
                    debug_name=None):
        text_variable = None
        if bg is None:
            bg = parent.cget('bg')
        if text is None:
            text_variable = StringVar()
        label = Label(parent,
                      text=text, textvariable=text_variable,
                      bg=bg, width=width, image=image,
                      anchor=anchor, justify=justify)
        if anchor == 'center':
            anchor = 'w'
        label.grid(row=row, column=col, sticky=anchor, columnspan=colspan)
        return GhAppHandle(text_variable, label, debug_name=debug_name)

    @staticmethod
    def createButton(parent, row, col,
                     command,
                     text,
                     anchor='w',
                     padx=0, pady=0,
                     width=None,
                     image=None,
                     text_visible=None,
                     debug_name=None):
        text_variable = StringVar()

        button = Button(parent, command=command, textvariable=text_variable,
                        anchor=anchor, padx=padx, pady=pady, width=width)
        button.grid(row=row, column=col, sticky=anchor)

        if text_visible or \
                not GhAppSetup.image_button \
                or GhAppSetup.image_text_button \
                or image is None:
            text_variable.set(text)

        if GhAppSetup.image_button:
            GhApp.setupImage(button, image, "left")
        return GhAppHandle(text_variable, button, debug_name=debug_name)

    @staticmethod
    def createRadio(parent, row, col, command,
                    text=None,
                    anchor='w',
                    padx=5,
                    debug_name=None):
        radiovar = IntVar()
        radio = Radiobutton(parent, bg=parent.cget('bg'), text=text,
                            command=command, variable=radiovar,
                            onvalue=1,
                            anchor=anchor, padx=padx)
        radio.grid(row=row, column=col, sticky=anchor)
        return GhAppHandle(radiovar, radio, debug_name=debug_name)

    @staticmethod
    def createCheckbox(parent, row, col, command,
                       text=None,
                       anchor='w',
                       padx=5,
                       debug_name=None):
        check_var = IntVar()
        check = Checkbutton(parent, bg=parent.cget('bg'), text=text,
                            command=command, variable=check_var,
                            onvalue=1,
                            anchor=anchor, padx=padx)
        check.grid(row=row, column=col, sticky=anchor)
        return GhAppHandle(check_var, check, debug_name=debug_name)

    @staticmethod
    def createCombobox(parent, row, col, command, values,
                       text=None,
                       anchor='w',
                       width=None,
                       colspan=1,
                       read_only=True,
                       debug_name=None):
        combo_var = StringVar()
        combo = Combobox(parent, text=text, width=width, textvariable=combo_var)
        combo.grid(row=row, column=col, columnspan=colspan, sticky=anchor)
        combo['values'] = values
        combo.bind('<<ComboboxSelected>>', command)
        if read_only:
            combo['state'] = 'readonly'
        return GhAppHandle(combo_var, combo, debug_name=debug_name)

    @staticmethod
    def createEntry(parent, row, col, width, defaultvalue,
                    padx=5, command=None,
                    colspan=1, sticky="w",
                    debug_name=None):
        entry_var = StringVar()
        entry_var.set(defaultvalue)
        entry = Entry(parent, textvariable=entry_var, width=width, validatecommand=command)
        entry.grid(row=row, column=col, columnspan=colspan, padx=padx, sticky=sticky)
        return GhAppHandle(entry_var, entry, debug_name=debug_name)
