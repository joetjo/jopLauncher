# jopLauncher

BUG : starting with exe don't work - prerequisite not managed properly by installer
<pre>
C:\Users\nicol\PycharmProjects\jopLauncher>dist\main.exe
Traceback (most recent call last):
  File "main.py", line 4, in <module>
    from launcher.core.procmgr import ProcMgr
  File "PyInstaller\loader\pyimod03_importers.py", line 540, in exec_module
  File "launcher\core\procmgr.py", line 3, in <module>
    import psutil
ModuleNotFoundError: No module named 'psutil'
[16108] Failed to execute script main
</pre>

