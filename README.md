# jop Game Launcher

> **SbSGL**

> No login/No internet access
> The Simple but Smart Game Launcher
> Old School GUI

Global game management platform that do not need internet, do not need any registering, do no store data into the cloud,
do not need to access to your game account.... and discover automatically which game is running ( with a light and
configurable prerequisite on where to install game ).

> All the recorded data are local and nothing is published. Local data are not protected ( protection rely on your local account on your laptop/desktop )

- Detects running game and record running time ( game has to be installed in a path that contains "jeux" , game process
  name will be used by default )
- Detect common game platform and display which one is running
- shows last gaming sessions and allows starting a new session of the corresponding game
- | -> or to search an already played game and allow to restart it
- | -> and applying a filter to see on installed game
- allows excluding process that are detected but are not game ( launcher, crash handler, etc.. you may discover strange
  things ).
- allows to map a custom name for an executable or to use the parent folder name instead of the executable name.
- allows customization on how to start a game ( launcher, alternative command line, parameters )
- allows linking on HTML page and a local document about each game

**Platform :** Windows ( python )
Note: the project is fully compatible to other platforms but tested only on Windows 10 and packaged only for Windows.

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

Edit SbSGL.json in home dir.

# What will be in next version ?

Last version is 2021.1.0509b

Enhancement:

- launch and detect discord
- platform starter menu added

# Known bugs

- search apply only on last sessions, not all...

# Known limitations

- mapping name may be identical to a real other process name when loading process - to check
- missing scrollbar or pagination on extended display for excluded game platform and launchers
- refresh notification close launchers or excluded game
- it's not possible to start a game in admin mode

# Next version content:

Fixes:

- mapping running game --> crash on end game
- starting a new game setup the initial total duration to the last played game.
- Regression : starting a mapping do not propose anymore to use PARENT by default
- Game may be detected before UI startup and then not displayed in GUI
- Closing GUI is not done on click and that's a shame

Bug tracking system : None yet. Will be setup when needed.

# Enhancement To be done

- add icon to game
- add a way to disable the running mode if not supported.
- add a way to add a specific process that do not map the pattern
- add pagination for all sessions
- packaging icons / images
- separate storage in multiple files
- on storage migration, save à backup of the file before
- menu to start "IconFx"
- double game for certain game to be supported...
- game associated to platform should not start if platform is not started based on a flag by platform ( steam start
  automatically for example )

# Potential Enhancement

- ui preference editor ( generic over GHSetup ) - top level panel with a generic property editor

# Major enhancement

- merge different storage when playing on several laptop/desktop

# Step to switch to public

- license decision
- header in file
- screenshots in readme
- reset local storage to no publish my data
- finalize packaging ( app icon, resources, ... )

# Minimal testing STABLE release

- delete storage and restart from empty stuff
- generates fake test executable ( bat files in `tests` folder ) and use fake exe to test
  - borderland 2 ( EPIC ) : Game that use natively a launcher to start the game
    - start Borderland 2 from folder
      `wait for detection`
    - stop
      `wait for detection`
    - edit game:
      - declare EPIC
      - select a custom path ( launcher.exe next to Borderland2.exe ) for Borderland2
      - set patch to Borderland2 in custom parameter
    - start borderland2 from SbSGL --> launcher and then fake borderland 2
      `wait for detection`
    - stop borderland2
    - exclude launcher from game detection ( check if visible in exclude gage )
      `wait for detection`

    `CAPTURE`

  - start AssassinsCreeds42 ( UBISOFT )  - mapping on a custom name
    `wait for detection`
    - stop
      `wait for detection`
    - edit game:
      - declare UBISOFT
    - map game to Assassins Creed - JoProd Arrival
    - start game from SbSGL --> game name should be ok
      `wait for detection`
    - stop game

  - start Control ( STEAM )  - default behavior
    `wait for detection`
    - stop
      `wait for detection`
    - edit game:
      - declare STEAM
    - start game from SbSGL
      `wait for detection`
    - stop game

  - start RoseOfSegunda\renpy.exe ( ITCHIO )  - name from parent folder ( generic executable common tu multiple game )
    `wait for detection`
    - stop
      `wait for detection`
    - edit game:
      - declare ITCHIO
    - map game to PARENT
    - start game from SbSGL
      `wait for detection`
    - stop game

``BROKEN`` --> tw3 visible twice in sessions storage

- start The Witcher 3 ( GOG )  - Modding case, setup a generic launcher to start it
  `wait for detection`
  - stop
    `wait for detection`
  - edit game:
    - declare GOG
    - setup mapping to PARENT
    - add a new launcher ( use aLauncher.exe from game folder
    - assign it to the witcher
  - start game from SbSGL --> Launcher will start game ( similar to Borderland case )
    `wait for detection`
  - stop game

- start The Witcher 2 - no store
  `wait for detection`
  - stop
    `wait for detection`
  - start game from SbSGL
    `wait for detection`
  - stop game

- start Mass Effect ...  ( ORIGIN ) - long name behaviour
  `wait for detection`
  - stop
    `wait for detection`
  - edit game:
    - declare ORIGIN
    - setup mapping to PARENT
  - start game from SbSGL
    `wait for detection`
  - stop game

Choose your favorite game and assign:

- a local markdown
- a store URL
- a Tips/Walktrough URL

Start Companion APP

Check launcher list

Check excluded game

Search game

Remove some Exe and filter with installed game

# Note:

- info about scrollbar : https://www.geeksforgeeks.org/scrollable-frames-in-tkinter/
- icon source set from https://icons8.com/icons ( Thanks to support Open Source project ! )