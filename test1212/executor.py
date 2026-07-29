import subprocess
import logging
import os

logger = logging.getLogger(__name__)

class CommandExecutor:
    """Runs shell commands when a pattern matches."""
    def __init__(self, timeout=10):
        self.timeout = timeout

    def run(self, cmd, extra_env=None):
        env = os.environ.copy()
        if extra_env:
            # cast everything to string just in case
            clean_env = {k: str(v) for k, v in extra_env.items()}
            env.update(clean_env)

        try:
            # shell=True is needed because users often put pipes or redirects in their config
            result = subprocess.run(
                cmd, 
                shell=True, 
                check=True, 
                timeout=self.timeout,
                env=env,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            logger.warning(f"command timed out after {self.timeout}s: {cmd}")
        except subprocess.CalledProcessError as e:
            logger.error(f"command failed (code {e.returncode}): {cmd}")
            if e.stderr:
                logger.debug(f"stderr: {e.stderr.strip()}")
        except Exception:
            logger.exception("unexpected error during execution")
        return None
