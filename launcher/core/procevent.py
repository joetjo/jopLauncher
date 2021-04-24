from abc import ABC, abstractmethod


class EventListener(ABC):
    pass

    @abstractmethod
    def newGame(self, proc):
        print("[ABC Impl] New game detected {} ({})".format(proc.getName(), proc.getPath()))

    @abstractmethod
    def endGame(self, proc):
        print("[ABC Impl] End game detected {} ({})".format(proc.getName(), proc.getPath()))
