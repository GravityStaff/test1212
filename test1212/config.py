import yaml
from dataclasses import dataclass
from typing import List

@dataclass
class Rule:
    name: str
    pattern: str
    command: str

@dataclass
class Config:
    path: str
    rules: List[Rule]

def load_config(file_path):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    rules = [Rule(**r) for r in data.get('rules', [])]
    return Config(path=data['path'], rules=rules)
