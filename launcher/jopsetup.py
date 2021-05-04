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
        self.initSetupEntry(self.APP_WIDTH, 850)
        self.initSetupEntry(self.APP_MIN_HEIGHT, 300)
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
        self.initSetupEntry(self.MAX_LAST_SESSION_COUNT, 10)
        self.initSetupEntry(self.GAME_PATTERN, 'jeux')
        self.initSetupEntry(self.GAME_EXTENSION, '.exe')
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
