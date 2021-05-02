import psutil

# All call to psutil is done here in order to be able to test without a real call
from launcher.log import Log


class ProcessUtil:

    def process_iter(self):
        return psutil.process_iter()

    def readProcessAttributes(self, process):
        try:
            return process.as_dict(attrs=['pid', 'name', 'exe'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            Log.info("--- unable to access process ---" + e)
            return None
