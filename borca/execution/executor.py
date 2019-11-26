from typing import List, Dict
import subprocess  # nosec

from borca.util import createLogger
from borca.parsing import Task


class Executor:
    def __init__(self, config: Dict, tasks: List[Task]) -> None:
        self.__config = config
        self.__tasks = tasks
        self.__logger = createLogger('borca.Executor', self.__config['verbosity'])

    def run(self) -> None:
        for task in self.__tasks:
            self.__logger.info(f"Executing task: {task.name}")
            for command in task.commands:
                self.__logger.debug(f"Running command: {command}")
                proc = subprocess.run(command, check=True)  # nosec

                # TODO: add caching stuff
