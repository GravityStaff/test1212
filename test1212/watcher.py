import re
import time
import os
from test1212.executor import run_command

class LogWatcher:
    def __init__(self, config):
        self.rules = config.get('rules', [])
        
    def run(self):
        # very basic polling for now
        paths = {r['path'] for r in self.rules}
        files = {path: open(path, 'r') for path in paths}
        
        for path, f in files.items():
            f.seek(0, os.SEEK_END)
            
        while True:
            for r in self.rules:
                f = files[r['path']]
                line = f.readline()
                if line and re.search(r['pattern'], line):
                    run_command(r['command'])
            time.sleep(0.1)
