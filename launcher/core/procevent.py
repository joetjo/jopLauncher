from abc import ABC, abstractmethod

from launcher.log import Log


class EventListener(ABC):
    pass

    @abstractmethod
    def newGame(self, proc):
        Log.debug("[ABC Impl] New game detected {} ({})".format(proc.getName(), proc.getPath()))

    @abstractmethod
    def refreshDone(self):
        pass

    @abstractmethod
    def endGame(self, proc):
        Log.debug("[ABC Impl] End game detected {} ({})".format(proc.getName(), proc.getPath()))
