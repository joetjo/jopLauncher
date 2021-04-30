# jop Game Launcher

Global game management platform that do not need internet, do not need any registering, do no store data into the cloud, do not need access to your game account....
and discover automatically which game is running ( with a prerequisite on where to install game ). 

> All the recorded data are local and nothing is published. Local data are not protected ( protection rely on your local account on your laptop/desktop )

- Detect running game and record running time ( game has to be installed in a path that contains "jeux" , game process name will be used by default )
- show last 10 gaming sessions and allow to restart corresponding game
- | -> or to search an already played game and allow to restart it 
- allow to exclude process that are detected but are not game ( launcher, crash handler, etc.. you may discover strange things ).
- allow to map a custom name for an executable or to use the parent folder name instead of the executable name.

**Platform :** Windows ( python )
Note: the project is fully compatible to other platforms but tested only on windows and packaged only for windows.

**Suggested Companion app**

A good companion app to take notes about your games : https://www.electronjs.org/apps/notable
it allows to set a markdown file by game and "tag" game to search in your own game. jopLauncher allows to link the md file of the game and to open it outside notable. What is interessant with notable is that is used standard markdown file that can used anywhere nut notable allows a nice tagging / indexing / searching / visualization.

# FAQ - Documentation

No manual available - here is the answer of the most common question

> My game use a generic launcher name use for many games, how automatic detection will deal with it ?

On first game that use the generic name, select it in history ( or search result ) and set a custom mapping using 'map' button' and set mapping to `PARENT`. Folder name will be used instead of executable name.

> My game executable name use ( automatic name ) is not really a good one, can I change it ?

Select game in history ( or search result ) and set a custom mapping using 'map'. Set the name you want instead of the original executable name.

> Jop Game Launcher has detect a process that is not a game, how to remove it ?

Select invalid game in history ( or search result ) and use `exclude` button. This executable will be removed and ignore if detected again. 
There is currently no way to cancel the executable exclusion using the application ( storage in json format has to be edited manually ).

> How to reset stat for a game ?

Select game in history  and use `remove` button. Game will appears back when launch.

> My game is not detected, what I can do ?

game has to be installed in a folder hierarchy that contains the pattern `jeux` ( not configurable yet )
not possible yet to add game manually in list.

> How to I change application setup ?

Not available

# What will be in next version ?

Last version is 2021.1.0425

Fixed:
- when displaying search result, all stuff is shift to the right ( minor, but all should be attached to the left... )
- select several games ( buttons appear ), unselect one buttons disappear and there is still some game selected... still
  some buttons visible on empty line.

Enhancement:

- playing : add current play time ( on each refresh ) and rework header panel
- launch game button
- partial ( launch game with a launcher but setup to be done manually in storage )
- excluded game display + remove from exclude list
- launcher display ( and remove launcher declaration )
- add top / left menu button
- detect running platform add show all gaming platform that is running

# Known bugs

- missing scrollbar on extended display for excluded game platform and launchers
- launcher setup cannot be done ( manual storage edit )
- exclude do not remove last_session ( game is removed, and ignores, just last_session is kept )
- mapping name may be identical to a real other process name when loading process - to check
 
# Enhancement To be done
- python fake exe that display just 1st parameter to test ( normal launch / launcher ) - GUI with just a label
- filter installed game
- packaging icons / images
- ui preference ( use GHSetup )
- add launcher list 
  - declare a new launcher
  - exclude launcher from game detection
  - associate launcher to a game
- add a way to select a different launcher that running execution + a way to disable the running mode if not supported.
- add a way to define a custom launcher
- separate storage in multiple files
- add a way to add a specific process that do not map the pattern
- add a way to add Game platform, check if running and allow to start them if not started
- add a way to reference a local md file from a "common" folder
- add a way to add a http link to store page
- add a way to add a http link to external link ( tips soluce or whatever =
- ui preference editor ( use GHSetup )
- on storage migration, save à backup of the file before

# Major enhancement
- merge different storage when playing on several laptop/desktop

# Step to switch to public
- license decision
- header in file
- screenshots in readme
- reset local storage to no publish my data

# Note:
- info about scrollbar : https://www.geeksforgeeks.org/scrollable-frames-in-tkinter/
