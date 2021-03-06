# Copyright 2022 joetjo https://github.com/joetjo/MarkdownHelper
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


class Strings:
    # Labels
    NO_GAME = "-"
    GAME_COUNT = "{} games (total) "
    PLAYING = "Playing"
    PREVIOUS = "Display mode [last sessions]"
    SEARCH = "| Search:"
    FILTER = "| Filter:"
    SEARCHING = "Display mode [Searching...please wait]"
    INSTALLED_FILTER = "installed"
    EXTENDED_FILTER = "extended"
    EXTENDED_FILTER_TOOLBAR = "Extended Filter:"
    PLAY_TIME = "Play time"
    TIME_PLAYED = "Total time"
    LAST_LAUNCH = "Last play"
    LAST_DURATION = "Last play duration"
    TOTAL_DURATION = "Total play time"
    GAME_NAME = "Game"
    MENU_EXCLUDED = "Show excluded games"
    MENU_LAUNCHER = "Show launchers"
    MENU_COMP_APP = "Companion App"
    MENU_MARKDOWN_REPORT = "Update Markdown Report"
    MENU_ICONFX_APP = "Icon App"
    LAUNCH_PLATFORM_MENU = ""
    EXCLUDED_GAME = "   ** Excluded games **  "
    LAUNCHERS = "   ** Custom launchers **  "
    PLATFORMS = "Actives Platforms"
    EXIT = "Quit"
    ERROR_INPUT = "Invalid input"
    LAUNCHER = "Launcher: "
    CUSTOM_LAUNCHER = "Custom command: "
    GAME_PLATFORM = "Platform: "
    CUSTOM_PARAMS = "Command parameters: "
    NEW_LAUNCHER = "+"
    SELECT_EXE_BUTTON = "..."
    SELECT_NOTE_BUTTON = "..."
    SELECT_EXE = "Select executable"
    SELECT_NOTE = "Select associated document"
    GAME_TYPE = "Type: "
    GAME_STATUS = "Status: "
    GAME_Note = "Note: "
    LOCAL_LINK = "Local notes: "
    WWW_LINK = "Game page: "
    TIPS_LINK = "Tips or whatever: "

    # Buttons
    SEARCH_ACTION = "  Go"
    ADD_FILTER_ACTION = "Add filter"
    DEL_FILTER_ACTION = "Remove Filter"
    APPLY_FILTER_ACTION = "OK"
    CANCEL_FILTER_ACTION = "Cancel"
    RESET_SEARCH_ACTION = "Reset"
    REFRESH_ACTION = "Refresh"
    EDIT_ACTION = " edit sheet"
    EDIT_APPLY_ACTION = " save edit"
    EDIT_CANCEL_ACTION = " cancel edit"
    IGNORE_ACTION = " exclude"
    REMOVE_ACTION = " remove"
    MAPPING_ACTION = " map"
    MAPPING_APPLY_ACTION = " apply mapping"
    MAPPING_CANCEL_ACTION = " cancel mapping"
    ABOUT_ACTION = "?"

    # Messages
    HELP_MAPPING = ("Display mode: [Help]\n- if name is a specific one but unrelated to game,--> set a custom name"
                    "                    \n- if name is a generic launcher, --> use PARENT to use parent folder name")
    RESULT_SEARCH_EXCEED = ("Display mode: [Search result: {} games] - only {} displayed\n"
                            "refine the token to find your game !")
    RESULT_SEARCH = "Display mode: [Search result: {} games]"
    CONFIRM_TITLE = "Please confirm !"
    CONFIRM_IGNORE_SELECTION = "{}:\n- {}"
    CONFIRM_IGNORE_APPLY = "Do you really want to exclude theses executable \n(Future execution will be ignored): "
    CONFIRM_REMOVE_APPLY = "Do you really want to remove data for theses files\n(Reset data without excluding): "
    EMPTY_NAME = "set a name for {}"
    CONFIRM_NEW_LAUNCHER = "Create a new launcher named:\n{}"
