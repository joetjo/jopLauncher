import os

import psutil

# All call to psutil is done here in order to be able to test without a real call
from JopLauncherConstant import JopLauncher
from launcher.log import Log


class ProcessUtil:

    def __init__(self, test):
        self.test_mode = test
        self.test_list = []
        self.test_attrs = dict()
        self.test_attrs["pid"] = 12

    def process_iter(self):
        if self.test_mode:
            return iter(self.test_list)
        else:
            return psutil.process_iter()

    def readProcessAttributes(self, process):
        if self.test_mode:
            return self.test_attrs
        try:
            return process.as_dict(attrs=['pid', 'name', 'exe'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            Log.info("--- unable to access process ---" + e)
            return None

    def test_setGame(self, game):
        if game is None:
            self.test_list = []
        else:
            self.test_list = [game]
            self.test_attrs["name"] = game
            self.test_attrs["exe"] = "{}the{}path{}{}{}{}Folder{}{}{}".format(os.path.sep, os.path.sep, os.path.sep,
                                                                       JopLauncher.GAME_PATTERN, os.path.sep,
                                                                       game, os.path.sep, game, JopLauncher.GAME_EXTENSION)

