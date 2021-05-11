import os
import subprocess
import threading


class GhLauncher:

    @staticmethod
    def launch(label, exe, cwd=os.getcwd()):
        print("Launching {} ({}) from folder {} ".format(label, exe, cwd))
        bg = threading.Thread(target=GhLauncher.launchImpl, args=(exe, cwd))
        bg.start()

    @staticmethod
    def launchImpl(exe, cwd):
        subprocess.run(exe, cwd=cwd)
