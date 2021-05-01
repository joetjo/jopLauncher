from JopLauncherConstant import JopLauncher
from launcher.log import Log


def nop(storage, version):
    Log.debug("| no data migration needed to upgrade to version {}".format(version))


class StorageVersion:
    VERSION_LIST = [0,
                    JopLauncher.DB_VERSION]

    MIGRATIONS_STEP = [nop,
                        nop]

    @staticmethod
    def check_migration(storage, to):
        if storage.getVersion() != to:
            current = storage.getVersion()
            Log.info("Storage migration from {} to {}".format(current, to))
            for idx in range(0,len(StorageVersion.VERSION_LIST)):
                v = StorageVersion.VERSION_LIST[idx]
                if current < v:
                    StorageVersion.MIGRATIONS_STEP[v](storage, v)
            storage.setVersion(to)
            storage.save()
