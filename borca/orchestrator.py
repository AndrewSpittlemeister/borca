from typing import Dict
from pathlib import Path

from borca.task import generateTasks, TaskGraph
from borca.util import createLogger
from borca.exceptions import InvalidTomlPath


class Orchestrator:
    def __init__(self, config: Dict) -> None:
        self.__config = config
        self.__logger = createLogger('borca.Orchestrator', self.__config['verbosity'])

        self.__toml = Path(self.__config['toml_path'])

        if (not self.__toml.exists()) or (not self.__toml.is_file()):
            raise InvalidTomlPath(f"Could not find pyproject.toml at {self.__config['toml-path']}")

        self.__toml.resolve()

        self.__logger.info(f"Using {self.__toml}")

        self.__graph = TaskGraph(self.__config, generateTasks(self.__config, self.__toml))

    def run(self) -> None:
        self.__graph.execute()
