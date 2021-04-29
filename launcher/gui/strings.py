

class Strings:
    # Labels
    NO_GAME = "-"
    PLAYING = "Playing"
    PREVIOUS = "Display mode [last sessions]"
    SEARCH = "| Search:"
    FILTER = "| Filter:"
    SEARCHING = "Display mode [Searching...please wait]"
    INSTALLED_FILTER = "installed"
    PLAY_TIME = "Play time"
    TIME_PLAYED = "Total time"
    LAST_LAUNCH = "Last play"
    LAST_DURATION = "Last play duration"
    TOTAL_DURATION = "Total play time"
    GAME_NAME = "Game"

    # Buttons
    SEARCH_ACTION = "  Go"
    RESET_SEARCH_ACTION = "Reset"
    REFRESH_ACTION = "Refresh"
    IGNORE_ACTION = "exclude"
    REMOVE_ACTION = "remove"
    MAPPING_ACTION = "map"
    MAPPING_APPLY_ACTION = "apply mapping"
    MAPPING_CANCEL_ACTION = "cancel mapping"
    ABOUT_ACTION = "?"

    # Messages
    HELP_MAPPING = ("Display mode: [Help]\n- if name is a specific one but unrelated to game,--> set a custom name"
                    "                    \n- if name is a generic launcher, --> use PARENT to use parent folder name")
    RESULT_SEARCH_EXCEED = ("Display mode: [Search result: {} games] - only {} displayed\n"
                            "refine the token to find your game !")
    RESULT_SEARCH = "Display mode: [Search result: {} games]"
    CONFIRM_TITLE= "Please confirm !"
    CONFIRM_IGNORE_SELECTION = "{}:\n- {}"
    CONFIRM_IGNORE_APPLY = "Do you really want to exclude theses executable \n(Future execution will be ignored): "
    CONFIRM_REMOVE_APPLY = "Do you really want to remove data for theses files\n(Reset data without excluding): "
    EMPTY_NAME = "Empty name !", "set a name for {}"
