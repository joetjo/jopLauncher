import subprocess
import threading


class GhLauncher:

    @staticmethod
    def launch(label, exe):
        print("Launching {} ({}) ".format(label, exe))
        bg = threading.Thread(target=GhLauncher.launchImpl, args=(exe,))
        bg.start()

    @staticmethod
    def launchImpl(exe):
        subprocess.run(exe)
