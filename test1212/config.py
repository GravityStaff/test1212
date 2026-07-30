import yaml
import os
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Rule:
    name: str
    pattern: str
    command: str
    timeout: int = 10

@dataclass
class Config:
    path: str
    rules: List[Rule] = field(default_factory=list)
    
    def __post_init__(self):
        if not os.path.exists(self.path):
            # it might be a pipe or a file that hasn't been created yet
            # but we should at least warn if the directory doesn't exist
            parent = os.path.dirname(os.path.abspath(self.path))
            if not os.path.exists(parent):
                raise FileNotFoundError(f"directory does not exist: {parent}")

def load_config(file_path: str) -> Config:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    if not data or 'path' not in data:
        raise ValueError("config must specify a log path")

    rule_list = []
    for r in data.get('rules', []):
        # FIXME: strictly validate regex pattern here before we start the watcher
        rule_list.append(Rule(
            name=r.get('name', 'unnamed'),
            pattern=r['pattern'],
            command=r['command'],
            timeout=r.get('timeout', 10)
        ))
    
    return Config(path=data['path'], rules=rule_list)
