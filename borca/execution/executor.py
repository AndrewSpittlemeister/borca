from typing import List, Dict, Tuple
import subprocess  # nosec

from borca.util import createLogger
from borca.parsing import Task


class Executor:
    def __init__(self, config: Dict, tasks: List[Task]) -> None:
        self.__config = config
        self.__tasks = tasks
        self.__logger = createLogger('borca.execution.Executor', self.__config['verbosity'])

    def run(self) -> Tuple[int, int, int]:
        completed_tasks: int = 0
        cached_tasks: int = 0

        for task in self.__tasks:
            self.__logger.info(f"Executing task: {task.name}")

            # TODO: add caching stuff here

            for command in task.commands:
                self.__logger.debug(f"Running command: {command}")

                if self.__config["verbosity"] == 0:
                    proc = subprocess.run(command, capture_output=True)  # nosec
                else:
                    proc = subprocess.run(command)  # nosec

                try:
                    proc.check_returncode()
                except subprocess.CalledProcessError as e:
                    self.__logger.error(
                        f"Error occurred in running command \"{command}\" under task \"{task.name}.\"\n{e}"
                    )
                    return len(self.__tasks), completed_tasks, cached_tasks

                self.__logger.debug(f"Completed command: {command}")

            self.__logger.info(f"Completed task: {task.name}")
            completed_tasks += 1

        return len(self.__tasks), completed_tasks, cached_tasks
