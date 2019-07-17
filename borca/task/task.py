from pathlib import Path
import json
from typing import List, Dict

import toml


class Task:
    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self) -> None:
        raise NotImplementedError


def generateTasks(config: Dict, tomlfile: Path) -> Dict[str, Task]:
    '''Load the tomlfile into memory and parse out borca config & tasks.'''

    toml_data = toml.load(str(tomlfile))
    print(json.dumps(toml_data, indent=4))

    toml_data['']
    exit(0)