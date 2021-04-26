# jop Game Launcher

Global game management platform that do not need internet, do not need any registering, do no store data into the cloud, do not need access to your game account....
and discover automatically which game is running ( with a prerequisite on where to install game ). 

> All the recorded data are local and nothing is published. Local data are not protected ( protection rely on your local account on your laptop/desktop )

- Detect running game and record running time ( game has to be installed in a path that contains "jeux" , game process name will be used by default )
- show last 10 gaming sessions and allow to restart corresponding game
- | -> or to search an already played game and allow to restart it 
- allow to exclude process that are detected but are not game ( launcher, crash handler, etc.. you may discover strange things ).
- allow to map a custom name for an executable or to use the parent folder name instead of the executable name.

Platform : **Windows** ( python )

Note: the project is fully compatible to other platform be tested only on windows and packaged only for windows.

# next version

> minor update
- update window app sizing

# Bug To be fix
- scrollbar / minimum size
- mapping name may be identical to a real other process name when loading process - to check
 
# Enhancement To be done
- ui preference ( use GHSetup )
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

# Step to switch to public
- license decision
- header in file
