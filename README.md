# jop Game Launcher

Game management platform that do not need internet, do not need any registering, do no store data into the cloud, do not need access to your game account....
and discover automatically which game is running ( with a prerequisite on where to install game ). 

> All the recored data are local and nothing is published.

- Detect running game and record running time ( game has to be installed in a path that contains "jeux" , game process name will be used by default )
- show last 10 gaming sessions and allow to start them
- | -> or to search an already played game and allow to start it 
- allow to exclude process that are detected but are not game ( launcher, crash handler, etc.. you may discover strange things ).
- allow to map a custom name for an executable or to use the parent folder name instead of the executable name.

# next version

Fixes:
- larger window
- better window placement at startup ( top right - my preference - not configurable yet)
- update last played on stating game ( with current total duration )
- fix alignment in session history
- setup a mapping keep old session in list ( bug ) and don't rename existing name in storage ( so 2 games exist )

Enhancements:
- add search in upper right and then previous session is replaced by search result
- remove exe extension from game name
- ui preference group in JopConstant ( but GhSetup not yet introduce ),
- |-> pattern token ( jeux ) and game extension ( .exe ) included but not configurable ( windows only, game pattern is frenchy )
- |-> history count entry also in constant ( with window height adjustement )
- show the original name on mapping when a mapping was already done

migration note:
- remove ".exe" from storage
- last sessions game list should be deleted

# Bug To be fix
- duration display is a date so 1 Jan 1970

# Enhancement To be done
- ui preference
- separate storage in multiple files
- add launcher button + a way to select a different launcher that running executation + a way to disable the running mode if not supported.
- add a way to define a custom launcher
- add a way to add a specific process that do not map the pattern
- add a way to add Game platform, check if running and allow to start them if not started
- add a way to reference a local md file from a "common" folder
- add a way to add an http link to store page
- add a way to add an http link to external link ( tips soluce or whatever =
- how to check and cancel ignored file

Test related:
- use a separate window to run the test mode

