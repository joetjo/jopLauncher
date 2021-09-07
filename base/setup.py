from pathlib import Path

from base.jsonstore import GhStorage


class GhSetup(GhStorage):

    def __init__(self, appname, content=None):
        if content is None:
            home = str(Path.home())
            self.filename = "{}/.{}.json".format(home, appname)
            super(GhSetup, self).__init__(self.filename)

            try:
                self.setup = self.data()['global']
            except KeyError:
                self.data()['global'] = {}
                self.save()
                self.setup = self.data()['global']

            print("GhSetup: Configuration loaded")
        else:
            super(GhSetup, self).__init__(appname, content)

    # get string value with name key
    def setup(self, key):
        try:
            return self.setup[key]
        except KeyError:
            self.setup[key] = ""
            return self.setup[key]

    # get bloc value with name key
    def getBloc(self, key):
        try:
            return self.content[key]
        except KeyError:
            self.content[key] = {}
            return self.content[key]
