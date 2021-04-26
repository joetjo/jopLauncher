from basegui.application import GhAppSetup


class JopLauncher:

    # To be updated on release
    TEST_MODE = False
    VERSION = '2021.1.4.0425.2'
    ###########################
    APP_NAME = 'Jop Game Launcher'
    SHORT_ABOUT = "JoProd@2021 by joetjo@Github"
    URL = "https://github.com/joetjo/jopLauncher"

    DB_VERSION = 1

    # delay between refresh 5s * REFRESH_DELAY
    REFRESH_DELAY = 10
    MAX_LAST_SESSION_COUNT = 10

    GAME_PATTERN = 'jeux'
    GAME_EXTENSION = '.exe'


# TODO - setup using GhSetup

GhAppSetup.width = 750
GhAppSetup.height = 200 + 20 * JopLauncher.MAX_LAST_SESSION_COUNT
GhAppSetup.vertical = 'top'
GhAppSetup.horizontal = 'right'

# GhAppSetup.vertical = 10
# GhAppSetup.horizontal = 10

# GhAppSetup.vertical = 'top'
# GhAppSetup.horizontal = 'center'
