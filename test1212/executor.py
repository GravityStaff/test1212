import subprocess
import logging

logger = logging.getLogger(__name__)

class CommandExecutor:
    def __init__(self, timeout=30):
        self.timeout = timeout

    def run(self, cmd):
        try:
            subprocess.run(cmd, shell=True, check=True, timeout=self.timeout)
        except subprocess.CalledProcessError as e:
            logger.error(f"command failed with exit code {e.returncode}: {cmd}")
        except Exception as e:
            logger.error(f"failed to run command: {e}")
