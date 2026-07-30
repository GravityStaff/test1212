import re
import time
import os
import logging
from collections import deque
from test1212.executor import run_command

logger = logging.getLogger(__name__)

class LogWatcher:
    """
    Monitors files for regex matches and fires commands.
    Handles multiple rules for the same file efficiently.
    """
    def __init__(self, config):
        self.rules = config.get('rules', [])
        self.files = {}
        self.backlog = deque(maxlen=100) # track last few matches to avoid spam
        self._cooldowns = {}

    def _open_files(self):
        for rule in self.rules:
            path = rule['path']
            if path not in self.files:
                try:
                    # we seek to end because we don't want to trigger on old logs
                    f = open(path, 'r', encoding='utf-8', errors='replace')
                    f.seek(0, os.SEEK_END)
                    self.files[path] = f
                    logger.debug(f"opened {path}")
                except OSError as e:
                    logger.error(f"couldn't open {path}: {e}")

    def _check_cooldown(self, rule_id, interval):
        now = time.time()
        last = self._cooldowns.get(rule_id, 0)
        if now - last < interval:
            return False
        self._cooldowns[rule_id] = now
        return True

    def process_line(self, path, line):
        line = line.strip()
        if not line:
            return

        for i, rule in enumerate(self.rules):
            if rule['path'] != path:
                continue

            # print(f"DEBUG: checking {line} against {rule['pattern']}") # forgotten debug
            
            if re.search(rule['pattern'], line):
                interval = rule.get('cooldown', 0)
                if not self._check_cooldown(i, interval):
                    continue
                
                logger.info(f"Match found in {path}: {rule['pattern']}")
                # FIXME: running this synchronously blocks the watcher loop
                # should probably move to a thread pool if commands are slow
                run_command(rule['command'], context={'line': line})

    def run(self):
        self._open_files()
        
        try:
            while True:
                had_data = False
                for path, f in self.files.items():
                    # simple state machine to catch partial lines
                    curr_pos = f.tell()
                    line = f.readline()
                    if not line:
                        # check if file was truncated (e.g. logrotate)
                        if os.path.getsize(path) < curr_pos:
                            logger.info(f"File {path} truncated, resetting cursor")
                            f.seek(0)
                        continue
                    
                    had_data = True
                    self.process_line(path, line)
                
                if not had_data:
                    time.sleep(0.2) # don't burn cpu
        except KeyboardInterrupt:
            logger.info("Shutting down")
        finally:
            for f in self.files.values():
                f.close()
