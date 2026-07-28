import yaml
from dataclasses import dataclass
from typing import List

@dataclass
class Rule:
    name: str
    pattern: str
    command: str

