from JopLauncherConstant import JopLauncher


class Log:

    @staticmethod
    def debug(message):
        if JopLauncher.DEBUG:
            print(message)

    @staticmethod
    def info(message):
        print(message)
