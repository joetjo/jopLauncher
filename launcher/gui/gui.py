from datetime import timedelta
from tkinter import StringVar, Label, Button

from basegui.application import GhApp, GhAppSetup
from launcher.core.procevent import EventListener

VERSION = '0.0.3'


class procGui(EventListener):
    label_width = 40

    def __init__(self, procmgr):
        self.procMgr = procmgr
        self.procMgr.setListener(self)

        GhAppSetup.height = 150
        self.app = GhApp("gGameScanner - {}".format(VERSION))

        # HEADER
        Label(self.app.header, text="Playing:", bg=GhAppSetup.bg_header,
              anchor="w", justify="left", width=procGui.label_width).grid(row=0, column=1)

        self.playing = StringVar()
        self.playingLabel = Label(self.app.header, bg=GhAppSetup.bg_header,
                                  anchor="w", textvariable=self.playing, width=30)
        self.playingLabel.grid(row=0, column=2)

        # CONTENT
        Label(self.app.content, text="Last played:", bg=GhAppSetup.bg_content,
              anchor="w", justify="left", width=procGui.label_width).grid(row=0, column=1)
        self.played = StringVar()
        self.playedLabel = Label(self.app.content, bg=GhAppSetup.bg_content,
                                 anchor="w", textvariable=self.played, width=30)
        self.playedLabel.grid(row=0, column=2)

        Label(self.app.content, text="Time played:", bg=GhAppSetup.bg_content,
              anchor="w", justify="left", width=procGui.label_width).grid(row=1, column=1)

        self.playedDuration = StringVar()
        self.playedDurationLabel = Label(self.app.content, bg=GhAppSetup.bg_content,
                                         anchor="w", textvariable=self.playedDuration, width=30)
        self.playedDurationLabel.grid(row=1, column=2)

        # FOOTER
        self.refresh = Button(self.app.status, text="Refresh", command=self.refresh)
        self.refresh.grid(row=0, column=1)

        proc = procmgr.getFirstMonitored()
        if proc is not None:
            self.setPlaying(proc)

        self.app.start()

    def refresh(self):
        self.procMgr.refresh()

    def setPlaying(self, proc):
        if proc is None:
            self.playing.set("")
        else:
            self.playing.set(proc.getName())
            self.setPlayedDuration(float(proc.getStoreEntry()["duration"]))

    def setPlayed(self, proc):
        self.played.set("{} | {}".format(proc.getName(), proc.getPlayedTime()))
        self.setPlayedDuration(float(proc.getStoreEntry()["duration"]))

    def setPlayedDuration(self, duration):
        delta = timedelta(seconds=duration)
        self.playedDuration.set(str(delta))

    # Proc listener implementations

    def newGame(self, proc):
        print("New game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(proc)

    def endGame(self, proc):
        print("End game detected {} ({})".format(proc.getName(), proc.getPath()))
        self.setPlaying(None)
        self.setPlayed(proc)
