from tkinter import Toplevel, Label, Button


class GhMessageBox:
    """
    message_type: warning, error, information, question
    """
    WARNING = "warning"
    ERROR = "error"
    INFO = "information"
    QUESTION = "question"

    def __init__(self, window, title, message, width=300, height=100, message_type="information",
                 on_ok=None, on_cancel=None):
        self.window = window
        self.title = title
        self.width = width
        self.height = height
        self.message = message
        self.message_type = message_type
        self.image = "::tk::icons::{}".format(message_type)
        self.on_ok = on_ok
        self.on_cancel = on_cancel
        self.top = None

    def show(self):

        self.window.wm_attributes("-disabled", True)

        shift_x = int(self.window.winfo_width() / 2 - self.width / 2)

        self.top = Toplevel(self.window)
        self.top.details_expanded = False
        self.top.title(self.title)
        self.top.geometry("{}x{}+{}+{}".format(self.width, self.height,
                                               self.window.winfo_x() + shift_x, self.window.winfo_y()))
        self.top.resizable(False, False)
        self.top.protocol("WM_DELETE_WINDOW", self.applyCancel)
        self.top.rowconfigure(0, weight=0)
        self.top.rowconfigure(1, weight=1)
        self.top.columnconfigure(0, weight=1)
        self.top.columnconfigure(1, weight=1)

        Label(self.top, image=self.image).grid(row=0, column=0, pady=(7, 0), padx=(7, 7), sticky="e")
        Label(self.top, text=self.message).grid(row=0, column=1, columnspan=3, pady=(7, 7), sticky="w")
        if self.on_ok is None:
            label_ok = "Close"
        else:
            label_ok = "OK"
        Button(self.top, text=label_ok, command=self.applyOk).grid(row=1, column=0, columnspan=2,
                                                                   sticky="s", padx=(7, 7), pady=(2, 5))
        if self.message_type == GhMessageBox.QUESTION or self.on_cancel is not None:
            Button(self.top, text="Cancel", command=self.applyCancel).grid(row=1, column=2,
                                                                           padx=(7, 7), pady=(2, 5), sticky="sw")
            Label(self.top, text="", width=5).grid(row=1, column=3, pady=(7, 7), sticky="n")

    def applyOk(self):
        self.close()
        if self.on_ok is not None:
            self.on_ok()

    def applyCancel(self):
        self.close()
        if self.on_cancel is not None:
            self.on_cancel()

    def close(self):
        self.window.wm_attributes("-disabled", False)
        self.top.destroy()
