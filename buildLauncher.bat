REM pip install pyinstaller
pyinstaller --onefile jopGameLauncher.py --hidden-import=tkinter --hidden-import=tkinter.messagebox
