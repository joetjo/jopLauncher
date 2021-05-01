from gridgui.application import GhAppSetup


class JopLauncher:
    # To be updated on release
    TEST_MODE = False
    VERSION = '2021.1.04.01.2'
    DEBUG = False
    ###########################
    APP_NAME = 'Jop Game Launcher'
    ABOUT = "SbSGL\nThe Simple but Smart Game Launcher\nOld School GUI\n[No login/No internet access]"
    SHORT_ABOUT = "JoProd@2021 by joetjo@Github"
    URL = "https://github.com/joetjo/jopLauncher"

    DB_VERSION = 2

    # delay between refresh 5s * REFRESH_DELAY
    REFRESH_DELAY = 10
    MAX_LAST_SESSION_COUNT = 10

    GAME_PATTERN = 'jeux'
    GAME_EXTENSION = '.exe'

    PLATFORM_WIDTH = 5
    GAME_NAME_WIDTH = 30
    URL_WIDTH = 70
    PARAMS_WIDTH = 45

    GAME_PLATFORMS = {
        "steam.exe": "STEAM",
        "GalaxyClient.exe": "GOG",
        "EpicGamesLauncher.exe": "EPIC",
        "upc.exe": "UBISOFT",
        "itch.exe": "ITCHIO",
        "Origin.exe": "ORIGIN"
    }

    EXEC_FILE = [("Executable", "*.exe"),
                 ("Batch file", "*.bat")]

    NOTE_FILE = [("Markdown", "*.md"),
                 ("Text", "*.txt"),
                 ("whatever you want", "*.*")]

    NOTE_EXE = "C:/Program Files (x86)/Notepad++/notepad++.exe"
    URL_EXE = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    LOCAL_FILE_FOLDER = "C:/Users/nicol/Documents/GitHub/gList/notes"
    COMPANION_APP = "C:/Users/nicol/AppData/Local/Programs/notable/Notable.exe"


# TODO - setup using GhSetup


GhAppSetup.width = 850
GhAppSetup.height = 300 + 24 * JopLauncher.MAX_LAST_SESSION_COUNT
GhAppSetup.vertical = 'top'
GhAppSetup.horizontal = 'right'
GhAppSetup.icon = 'icons/joystick.ico'

GhAppSetup.image_button = False
# Must not be false if image_button is false
GhAppSetup.image_text_button = True

# GhAppSetup.vertical = 10
# GhAppSetup.horizontal = 10

# GhAppSetup.vertical = 'top'
# GhAppSetup.horizontal = 'center'
