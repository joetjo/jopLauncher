from basegui.application import GhAppSetup


class JopLauncher:

    # To be updated on release
    TEST_MODE = True
    VERSION = '2021.1.wip'
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
GhAppSetup.icon = 'icons/joystick.ico'

GhAppSetup.image_button = True
# Must not be false if image_button is false
GhAppSetup.image_text_button = True

# GhAppSetup.vertical = 10
# GhAppSetup.horizontal = 10

# GhAppSetup.vertical = 'top'
# GhAppSetup.horizontal = 'center'
