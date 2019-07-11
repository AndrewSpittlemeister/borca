from pathlib import Path
from typing import List, Dict


class Task:
    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self) -> None:
        raise NotImplementedError


def generateTasks(config: Dict, tomlfile: Path) -> List[Task]:
    raise NotImplementedError
