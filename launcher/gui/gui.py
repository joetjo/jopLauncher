from datetime import timedelta
from tkinter import StringVar, Label, Button, Entry

from basegui.application import GhApp, GhAppSetup, GhColumnPanel
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
        footer = GhColumnPanel(self.app.footer)
        self.refresh = Button(footer.left, text="Refresh", command=self.refresh)
        self.refresh.grid()

        if self.procMgr.testmode:
            self.testgame = StringVar()
            self.testgameButton = StringVar()
            self.testgameButton.set("Start")
            self.testgame.set("jopLauncherTest")
            self.testgameEntry = Entry(footer.right, textvariable=self.testgame, width=15)
            self.startstop = Button(footer.right, textvariable=self.testgameButton, anchor="e", command=self.test_startstop)

            Label(footer.right, bg=GhAppSetup.bg_header, text="**TEST**").grid(row=0, padx=5)
            self.testgameEntry.grid(row=0, column=1, padx=5)
            self.startstop.grid(row=0, column=2)

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

    # TEST MODE PURPOSE ONLY
    def test_startstop(self):
        if len(self.playing.get()) == 0:
            self.procMgr.test_setgame(self.testgame.get())
            self.testgameButton.set("Stop")
        else:
            self.procMgr.test_setgame(None)
            self.testgameButton.set("Start")
