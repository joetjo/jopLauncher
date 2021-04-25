

class Strings:
    # Labels
    NO_GAME = "-"
    PLAYING = "Playing:"
    PREVIOUS = "Previous sessions:"
    SEARCH = "| Search:"
    SEARCHING = "Searching..."
    LAST_PLAYED = "Last played:"
    TIME_PLAYED = "Time played:"
    LAST_LAUNCH = "Last play"
    LAST_DURATION = "Last play duration"
    TOTAL_DURATION = "Total play time"
    GAME_NAME = "Game"

    # Buttons
    SEARCH_ACTION = "Go"
    RESET_SEARCH_ACTION = "Reset"
    REFRESH_ACTION = "Refresh"
    IGNORE_ACTION = "x"
    MAPPING_ACTION = "map"
    MAPPING_APPLY_ACTION = "apply mapping"
    MAPPING_CANCEL_ACTION = "cancel mapping"
    ABOUT_ACTION = "?"

    # Messages
    HELP_MAPPING = ("if name is a specific one\n but unrelated to game,\n--> set a custom name\n"
                    "\nif name is a generic launcher,\n --> use PARENT to use \nparent folder name")
    RESULT_SEARCH_EXCEED = ("Search result: {} games,\n\n only {} displayed\n"
                            "\nrefine the token \nto find your game !")
    RESULT_SEARCH = "Search result: {} games"
    CONFIRM_TITLE= "Please confirm !"
    CONFIRM_IGNORE_SELECTION = "{}:\n- {}"
    CONFIRM_IGNORE_APPLY = "Do you really want to ignore theses files: "
    EMPTY_NAME = "Empty name !", "set a name for {}"
