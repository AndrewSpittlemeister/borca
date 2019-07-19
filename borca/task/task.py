from pathlib import Path
import json
from typing import List, Dict

import toml


class Task:
    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self) -> None:
        raise NotImplementedError
