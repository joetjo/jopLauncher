from basegui.application import GhAppSetup


class JopLauncher:
    APP_NAME = 'JopLauncher'
    VERSION = '0.1.0'
    SHORT_ABOUT = "JoProd@2021 by joetjo@Github"
    URL = "https://github.com/joetjo/jopLauncher"

    # delay between refresh 5s * REFRESH_DELAY
    REFRESH_DELAY = 10
    MAX_LAST_SESSION_COUNT = 10
    TEST_MODE = False

    GAME_PATTERN = 'jeux'
    GAME_EXTENSION = '.exe'


# TODO - setup using GhSetup

GhAppSetup.width = 700
GhAppSetup.height = 200 + 20 * JopLauncher.MAX_LAST_SESSION_COUNT
GhAppSetup.vertical = 'top'
GhAppSetup.horizontal = 'right'

# GhAppSetup.vertical = 10
# GhAppSetup.horizontal = 10

# GhAppSetup.vertical = 'top'
# GhAppSetup.horizontal = 'center'
