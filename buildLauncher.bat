REM pip install pyinstaller
pyinstaller --onefile jopLauncher.py --hidden-import=tkinter --hidden-import=tkinter.messagebox
