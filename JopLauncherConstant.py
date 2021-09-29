from gridgui.application import GhAppSetup
from launcher.jopsetup import JopSetup

# True for print_mode
JopSETUP = JopSetup(False)


class JopLauncher:
    # To be updated on release
    VERSION = '2021.1.0929a'
    DEBUG = False
    ###########################
    APP_NAME = 'Jop Game Launcher'
    ABOUT = "SbSGL\nThe Simple but Smart Game Launcher\nOld School GUI\n[No login/No internet access]"
    SHORT_ABOUT = "JoProd@2021 by joetjo@Github"
    URL = "https://github.com/joetjo/jopLauncher"
    ICON_URL = "https://icons8.com"

    DB_VERSION = 2

    GAME_PLATFORMS = {
        "steam.exe": JopSETUP.STEAM,
        "GalaxyClient.exe": JopSETUP.GOG,
        "EpicGamesLauncher.exe": JopSETUP.EPIC,
        "upc.exe": JopSETUP.UBISOFT,
        "itch.exe": JopSETUP.ITCHIO,
        "Origin.exe": JopSETUP.ORIGIN
    }

    COM_APP_DISCORD = "Discord"
    COM_APP = {
        "Discord.exe": COM_APP_DISCORD
    }

    EXEC_FILE = [("Executable", "*.exe"),
                 ("Batch file", "*.bat")]

    NOTE_FILE = [("Markdown", "*.md"),
                 ("Text", "*.txt"),
                 ("whatever you want", "*.*")]


GhAppSetup.width = JopSETUP.get(JopSETUP.APP_WIDTH)
GhAppSetup.height = JopSETUP.get(JopSETUP.APP_MIN_HEIGHT) + \
                    (JopSETUP.get(JopSETUP.APP_HEIGHT_BY_GAME) * JopSETUP.get(JopSETUP.MAX_LAST_SESSION_COUNT))
GhAppSetup.vertical = JopSETUP.get(JopSETUP.APP_VERTICAL)
GhAppSetup.horizontal = JopSETUP.get(JopSETUP.APP_HORIZONTAL)
GhAppSetup.icon = JopSETUP.get(JopSETUP.APP_ICON)
GhAppSetup.theme = JopSETUP.get(JopSETUP.APP_THEME)

GhAppSetup.image_button = JopSETUP.get(JopSETUP.APP_IMAGE_BUTTON)
# Must not be false if image_button is false
GhAppSetup.image_text_button = JopSETUP.get(JopSETUP.APP_IMAGE_TEXT)

# GhAppSetup.vertical = 10
# GhAppSetup.horizontal = 10

# GhAppSetup.vertical = 'top'
# GhAppSetup.horizontal = 'center'
