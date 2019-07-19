from typing import Dict
from pathlib import Path

import toml

from borca.parsing import BorcaDatagram
from borca.task import TaskGraph
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

        self.__toml_data = toml.load(str(self.__toml))

        self.__datagram = BorcaDatagram(self.__config, self.__toml_data)

        self.__graph = TaskGraph(self.__config, self.__datagram.getTaskMap())

    def run(self) -> None:
        self.__graph.execute()
