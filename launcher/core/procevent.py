from abc import ABC, abstractmethod

from launcher.log import Log


class EventListener(ABC):
    pass

    @abstractmethod
    def newGame(self, game):
        Log.debug("[ABC Impl] New game detected {} ({})".format(game.getName(), game.process.getPath()))

    @abstractmethod
    def refreshDone(self, current_game, platform_list_updated, others):
        pass

    @abstractmethod
    def endGame(self, proc):
        Log.debug("[ABC Impl] End game detected {} ({})".format(proc.getName(), proc.getPath()))
