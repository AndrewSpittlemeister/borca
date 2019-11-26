from typing import List

from pydantic import BaseModel as PydanticBaseModel


class Task(PydanticBaseModel):
    name: str
    commands: List[str]
    depends_on: List[str] = []
    input_paths: List[str] = []
    output_paths: List[str] = []

    # not to be parsed, but for DAG building
    dependencies: set = set()

    def __hash__(self) -> int:
        return int("".join([str(ord(character)) for character in self.name]))

    def __eq__(self, other) -> bool:
        return self.name == other.name


class BorcaData(PydanticBaseModel):
    default_task: str
    tasks: List[Task]
