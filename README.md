# jopLauncher

Detect running game and record running time ( game has to be installed in a path that contains "jeux" , game process name will be used by default )

Other feature:
- show last 10 gaming sessions
- allow to exclude process
- allow to map a custom name for an exe or to use the parent folder name instead of the executable name.

# next version

Fixes:
- larger window
- better window placement at startup ( top right - my preference - not configurable yet)
- update last played on stating game ( with current total duration )
- fix alignment in session history

Enhancements:
- add search in upper right and then previous session is replaced by search result
- remove exe extension from game name

migration note:
- remove ".exe" from storage

# Bug To be fix
- setup a mapping keep old session in list ( bug ) and don't rename existing name in storage ( so 2 games exist )

# Enhancement To be done
- ui preference
- add launcher button + a way to select a different launcher that running executation + a way to disable the running mode if not supported.
- token "jeux" should be customizable
- history count 10 should be configurable ( en window height should be adpated to history size )
