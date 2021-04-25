from basegui.application import GhAppSetup


class JopLauncher:
    APPNAME = 'JopLauncher'
    VERSION = '0.1.0'
    # delay between refresh 5s * REFRESH_DELAY
    REFRESH_DELAY = 10
    MAX_LAST_SESSION_COUNT = 10

GhAppSetup.width = 660
GhAppSetup.height = 200 + 20 * JopLauncher.MAX_LAST_SESSION_COUNT
GhAppSetup.vertical = 'top'
GhAppSetup.horizontal = 'right'

#GhAppSetup.vertical = 10
#GhAppSetup.horizontal = 10

#GhAppSetup.vertical = 'top'
#GhAppSetup.horizontal = 'center'
