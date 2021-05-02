from tkinter import PhotoImage

from base.fileutil import GhFileUtil
from launcher.log import Log


class GhIcons:
    ICON_PACK = "-26.png"

    def __init__(self, platforms):
        self.REFRESH = PhotoImage(file="icons/refresh" + GhIcons.ICON_PACK)

        self.PLATFORMS = dict()
        for p in platforms:
            acronym = platforms[p]
            file = "icons/platforms/{}.png".format(acronym)
            if GhFileUtil.fileExist(file):
                self.PLATFORMS[acronym] = PhotoImage(file=file)
            else:
                Log.info("No icon for platform {}".format(acronym))
                self.PLATFORMS[acronym] = None
