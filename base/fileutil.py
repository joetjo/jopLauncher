import os
import string
from pathlib import Path
from tkinter import filedialog

VALID_CHARS_4_FILENAME = "-_.() {}{}".format(string.ascii_letters, string.digits)


class GhFileUtil:

    @staticmethod
    def normalizeFileName(file):
        return ''.join(c for c in file if c in VALID_CHARS_4_FILENAME)

    @staticmethod
    def fileExist(file):
        return Path(file).is_file()

    @staticmethod
    def folderExist(file):
        return Path(file).is_dir()

    @staticmethod
    def home():
        return str(Path.home())

    @staticmethod
    def basenameWithExtent(file):
        return Path(file).stem

    @staticmethod
    def parentFolder(file):
        path = Path(file)
        return path.parent.absolute()

    @staticmethod
    def fileSelection(initialdir=os.getcwd(),
                      title="Select file",
                      filetypes=[("Text Files", "*.txt")]):
        return filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=filetypes)
