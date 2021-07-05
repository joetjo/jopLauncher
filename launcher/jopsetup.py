from pathlib import Path

from base.setup import GhSetup


# Setup definition for ZikRandomizer
# Setup file is stored in home folder: .ZikMgr.json
# - FOLDER  # folder path on desktop/laptop
# - TARGET  # audio device folder path when mounted
# - BACKUP  # folder path on desktop/laptop where removed file are stored
# - EXTENT  # file extent to use
# - TAG  # prefix used to randomize file


class JopSetup:
    _global_setup_ = None
    APP_WIDTH = "APP_WIDTH"
    APP_MIN_HEIGHT = "APP_MIN_HEIGHT"
    APP_HEIGHT_BY_GAME = "APP_HEIGHT_BY_GAME"
    APP_VERTICAL = "APP_VERTICAL"
    APP_HORIZONTAL = "APP_HORIZONTAL"
    APP_ICON = "APP_ICON"
    APP_THEME = "APP_THEME"
    APP_IMAGE_BUTTON = "APP_IMAGE_BUTTON"
    APP_IMAGE_TEXT = "APP_IMAGE_TEXT"
    GAME_NAME_WIDTH = "GAME_NAME_WIDTH"
    URL_WIDTH = "URL_WIDTH"
    PARAMS_WIDTH = "PARAMS_WIDTH"
    REFRESH_DELAY = "REFRESH_DELAY"
    MAX_LAST_SESSION_COUNT = "MAX_LAST_SESSION_COUNT"
    GAME_PATTERN = "GAME_PATTERN"
    GAME_EXTENSION = "GAME_EXTENSION"
    NOTE_EXE = "NOTE_EXE"
    URL_EXE = "URL_EXE"
    LOCAL_FILE_FOLDER = "LOCAL_FILE_FOLDER"
    COMPANION_APP = "COMPANION_APP"
    ICONFX_APP = "ICONFX_APP"
    DISCORD = "DISCORD"

    STEAM = "STEAM"
    GOG = "GOG"
    EPIC = "EPIC"
    UBISOFT = "UBISOFT"
    ITCHIO = "ITCHIO"
    ORIGIN = "ORIGIN"

    @staticmethod
    # Test Purpose
    def initJopSetup(content):
        JopSetup._global_setup_ = JopSetup(content)

    @staticmethod
    def getJopSetup():
        return JopSetup._global_setup_

    def __init__(self, print_mode, content=None):
        home = str(Path.home())
        self.print_mode = print_mode

        self.SETUP = GhSetup('SbSGL', content)

        self.ZMGR = self.SETUP.getBloc('SbSGL')

        self.dirty = False
        if print_mode:
            print("================= SbSGM SETUP  =========================")
        self.initSetupEntry(self.APP_WIDTH, 1050)
        self.initSetupEntry(self.APP_MIN_HEIGHT, 400)
        self.initSetupEntry(self.APP_HEIGHT_BY_GAME, 24)
        self.initSetupEntry(self.APP_VERTICAL, 'top')
        self.initSetupEntry(self.APP_HORIZONTAL, 'right')
        self.initSetupEntry(self.APP_ICON, 'icons/joystick.ico')
        self.initSetupEntry(self.APP_THEME, 'black')
        self.initSetupEntry(self.APP_IMAGE_BUTTON, True)
        self.initSetupEntry(self.APP_IMAGE_TEXT, False)
        self.initSetupEntry(self.GAME_NAME_WIDTH, 30)
        self.initSetupEntry(self.URL_WIDTH, 70)
        self.initSetupEntry(self.PARAMS_WIDTH, 45)
        self.initSetupEntry(self.REFRESH_DELAY, 5)
        self.initSetupEntry(self.MAX_LAST_SESSION_COUNT, 30)
        self.initSetupEntry(self.GAME_PATTERN, 'jeux')
        self.initSetupEntry(self.GAME_EXTENSION, '.exe')
        self.initSetupEntry(self.NOTE_EXE, "C:/Program Files (x86)/Notepad++/notepad++.exe")
        self.initSetupEntry(self.URL_EXE, "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")
        self.initSetupEntry(self.LOCAL_FILE_FOLDER, "C:/Users/nicol/Documents/GitHub/gList/notes")
        self.initSetupEntry(self.COMPANION_APP, ["C:/Users/nicol/AppData/Local/Programs/notable/Notable.exe"])
        self.initSetupEntry(self.ICONFX_APP, ["G:/NMPTF-PortableApps/PortableApps/IcoFXPortable/IcoFXPortable.exe"])
        self.initSetupEntry(self.DISCORD, ["C:/Users/nicol/AppData/Local/Discord/Update.exe",
                                           "--processStart",
                                           "Discord.exe"])

        self.initSetupEntry(self.STEAM, ["C:/Program Files (x86)/Steam/Steam.exe"])
        self.initSetupEntry(self.GOG, ["C:/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"])
        self.initSetupEntry(self.EPIC,
                            ["C:/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"])
        self.initSetupEntry(self.ITCHIO, ["G:/itchio/itch-setup.exe", "--prefer-launch" "--appname" "itch"])
        self.initSetupEntry(self.UBISOFT, ["C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/Uplay.exe"])
        self.initSetupEntry(self.ORIGIN, ["C:/Program Files (x86)/Origin/Origin.exe"])

        #        self.initSetupEntry(self., )
        if print_mode:
            print("========================================================")

        if self.dirty:
            self.save()

    def initSetupEntry(self, name, default_value):
        value = None
        reset = ""
        try:
            value = self.ZMGR[name]
        except KeyError:
            self.ZMGR[name] = default_value
            value = default_value
            result = "- [reset to default value]"
            self.dirty = True
        if self.print_mode:
            print(">>>>>>> {}: {}{}".format(name, value, reset))

    # set property value and generate KeyError is this is not a supported key entry
    # return previous value
    def set(self, name, value):
        old = self.ZMGR[name]
        self.ZMGR[name] = value
        if not self.dirty:
            print("Setup has been modified and has to be saved")
            self.dirty = True
        return old

    # get property value and generate KeyError is this is not a supported key entry
    def get(self, name):
        return self.ZMGR[name]

    def save(self):
        self.SETUP.save()
        self.dirty = False
