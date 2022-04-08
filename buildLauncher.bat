REM pip install pyinstaller
pyinstaller --onefile --noconsole --icon=joystick.ico jopGameLauncher.py --hidden-import=tkinter --hidden-import=tkinter.messagebox
