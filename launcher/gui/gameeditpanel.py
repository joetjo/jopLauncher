from JopLauncherConstant import JopLauncher, JopSETUP
from base.fileutil import GhFileUtil
from gridgui.application import GhApp
from gridgui.simplepanel import GhSimplePanel
from launcher.gui.strings import Strings
from launcher.log import Log


class GameEditPanel(GhSimplePanel):
    def __init__(self, parent, app, row, col, colspan=1, sticky="nsew"):
        super().__init__(parent, row=row, col=col, colspan=colspan, sticky=sticky)

        self.app = app
        self.session = None
        self.launcher_ok = True
        content = self.content

        self.row_reset()
        # Line 1
        self.ui_launcher_label = GhApp.createLabel(content, self.row(), self.col_next(), text=Strings.LAUNCHER)
        self.ui_launcher_combo = GhApp.createCombobox(content, self.row(), self.col_next(),
                                                      self.applyLauncher, self.app.procMgr.getLaunchers(),
                                                      width=8)
        self.ui_launcher_button = GhApp.createButton(content, self.row(), self.col_next(), text=Strings.NEW_LAUNCHER,
                                                     command=self.applyNewLauncher, image=self.app.icons.PLUS)
        self.ui_params_label = GhApp.createLabel(content, self.row(), self.col_next(), text=Strings.CUSTOM_PARAMS)
        self.ui_params = GhApp.createEntry(content, self.row(), self.col_next(), JopSETUP.get(JopSETUP.PARAMS_WIDTH),
                                           "", colspan=2)

        # Line 2
        self.row_col_reset(1, 0)
        self.ui_game_platform_label = GhApp.createLabel(content, self.row(), self.col_next(),
                                                        text=Strings.GAME_PLATFORM)
        self.ui_game_platform_combo = GhApp.createCombobox(content, self.row(), self.col_reset(3),
                                                           self.applyPlatform, self.app.procMgr.getPossiblePlatforms(),
                                                           width=8, colspan=2)
        self.ui_custom_label = GhApp.createLabel(content, self.row(), self.col_next(), text=Strings.CUSTOM_LAUNCHER)
        self.ui_custom_path = GhApp.createLabel(content, self.row(), self.col_next(),
                                                width=JopSETUP.get(JopSETUP.PARAMS_WIDTH))
        self.ui_custom_button = GhApp.createButton(content, self.row(), self.col_next(), text=Strings.SELECT_EXE_BUTTON,
                                                   command=self.applySelectExe, anchor="e",
                                                   image=self.app.icons.FILE_SELECTION)

        self.row_col_reset(2, 0)

        # Line 3
        self.ui_local_link_label = GhApp.createLabel(content, self.row(), self.col_next(),
                                                     text=Strings.LOCAL_LINK)
        self.ui_local_link = GhApp.createLabel(content, self.row(), self.col_reset(5), colspan=4)
        self.ui_local_button = GhApp.createButton(content, self.row_next(), self.col_reset(0),
                                                  text=Strings.SELECT_NOTE_BUTTON, image=self.app.icons.FILE_SELECTION,
                                                  command=self.applySelectLocal, anchor="e")

        # Line 4
        self.ui_www_link_label = GhApp.createLabel(content, self.row(), self.col_next(),
                                                   text=Strings.WWW_LINK)
        self.ui_www_link = GhApp.createEntry(content, self.row_next(), self.col_reset(),
                                             JopSETUP.get(JopSETUP.URL_WIDTH),
                                             "", colspan=5)

        # Line 5
        self.ui_tips_link_label = GhApp.createLabel(content, self.row(), self.col_next(),
                                                    text=Strings.TIPS_LINK)
        self.ui_tips_link = GhApp.createEntry(content, self.row(), self.col_reset(),
                                              JopSETUP.get(JopSETUP.URL_WIDTH),
                                              "", colspan=5)

    def grid_remove(self):
        super().grid_remove()
        self.ui_launcher_label.grid_remove()
        self.ui_launcher_combo.grid_remove()
        self.ui_custom_label.grid_remove()
        self.ui_custom_path.grid_remove()
        self.ui_custom_button.grid_remove()
        self.ui_game_platform_label.grid_remove()
        self.ui_game_platform_combo.grid_remove()
        self.ui_params_label.grid_remove()
        self.ui_params.grid_remove()
        self.ui_local_link_label.grid_remove()
        self.ui_local_link.grid_remove()
        self.ui_local_button.grid_remove()
        self.ui_www_link_label.grid_remove()
        self.ui_www_link.grid_remove()
        self.ui_tips_link_label.grid_remove()
        self.ui_tips_link.grid_remove()

    def grid(self):
        super().grid()
        self.ui_launcher_label.grid()
        self.ui_launcher_combo.grid()
        self.ui_custom_label.grid()
        self.ui_custom_path.grid()
        self.ui_custom_button.grid()
        self.ui_game_platform_label.grid()
        self.ui_game_platform_combo.grid()
        self.ui_params_label.grid()
        self.ui_params.grid()
        self.ui_local_link_label.grid()
        self.ui_local_link.grid()
        self.ui_local_button.grid()
        self.ui_www_link_label.grid()
        self.ui_www_link.grid()
        self.ui_tips_link_label.grid()
        self.ui_tips_link.grid()

    def set(self, session):
        self.session = session
        self.ui_launcher_combo.set(session.getLauncher())
        self.ui_game_platform_combo.set(session.getPlatform())
        self.ui_custom_path.set(session.getCustomCommand())
        self.ui_params.set(session.getParameters())
        self.ui_local_link.set(session.getNote())
        self.ui_www_link.set(session.getWWW())
        self.ui_tips_link.set(session.getTips())

    def updateStorage(self):
        session = self.session
        session.setLauncher(self.ui_launcher_combo.get())
        session.setPlatform(self.ui_game_platform_combo.get())
        session.setCustomCommand(self.ui_custom_path.get())
        session.setParameters(self.ui_params.get())
        session.setNote(self.ui_local_link.get())
        session.setWWW(self.ui_www_link.get())
        session.setTips(self.ui_tips_link.get())

    def isLauncherOk(self):
        return self.launcher_ok

    def applyLauncher(self, event):
        Log.debug("Launcher {} selected".format(self.ui_game_platform_combo.get()))

    def applyNewLauncher(self):
        folder = GhFileUtil.home()
        if GhFileUtil.fileExist(self.session.getPath()):
            folder = GhFileUtil.parentFolder(self.session.getPath())
        path = GhFileUtil.fileSelection(folder,
                                        title=Strings.SELECT_EXE,
                                        filetypes=JopLauncher.EXEC_FILE)
        if path is not None and len(path) > 0:
            name = GhFileUtil.basenameWithExtent(path)
            self.app.procMgr.addLauncher(name, path)
            self.ui_launcher_combo.set(name)

    def applyPlatform(self, event):
        Log.debug("Platform {} selected".format(self.ui_game_platform_combo.get()))

    def applySelectExe(self):
        folder = GhFileUtil.home()
        if GhFileUtil.fileExist(self.session.getPath()):
            folder = GhFileUtil.parentFolder(self.session.getPath())
        elif GhFileUtil.fileExist(self.session.getCustomCommand()):
            folder = GhFileUtil.parentFolder(self.session.getCustomCommand())
        path = GhFileUtil.fileSelection(folder,
                                        title=Strings.SELECT_EXE,
                                        filetypes=JopLauncher.EXEC_FILE)
        if path is not None and len(path) > 0:
            self.ui_custom_path.set(path)

    def applySelectLocal(self):
        folder = GhFileUtil.home()
        if len(self.session.getNote()) > 0:
            folder = GhFileUtil.parentFolder(self.session.getNote())
        else:
            folder = JopSETUP.get(JopSETUP.LOCAL_FILE_FOLDER)
        path = GhFileUtil.fileSelection(folder,
                                        title=Strings.SELECT_NOTE,
                                        filetypes=JopLauncher.NOTE_FILE)
        if path is not None and len(path) > 0:
            self.ui_local_link.set(path)
