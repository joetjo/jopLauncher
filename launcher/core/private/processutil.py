import psutil


# All call to psutil is done here in order to be able to test without a real call
class ProcessUtil:

    def __init__(self, test):
        self.testmode = test
        self.testlist = []
        self.testattrs = dict()
        self.testattrs["pid"] = 12

    def process_iter(self):
        if self.testmode:
            return iter(self.testlist)
        else:
            return psutil.process_iter()

    def readProcessAttributes(self, process):
        if self.testmode:
            return self.testattrs
        try:
            return process.as_dict(attrs=['pid', 'name', 'exe'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print("--- unable to access process ---" + e)
            return None

    def test_setgame(self, game):
        if game is None:
            self.testlist = []
        else:
            self.testlist = [game]
            self.testattrs["name"] = game
            self.testattrs["exe"] = "/the/path/jeux/{}/{}.exe".format(game, game)

