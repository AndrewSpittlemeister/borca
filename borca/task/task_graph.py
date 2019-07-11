from typing import List, Dict

from borca.task import Task
from borca.util import createLogger


class TaskGraph:
    def __init__(self, config: Dict, tasks: List[Task]) -> None:
        self.__config = config
        self.__taskList = tasks
        self.__logger = createLogger('borca.TaskGraph', self.__config['verbosity'])

        self.root: Task = self.__buildLinkedGraph()

        self.__logger.info('Successfully constructed acyclic task graph.')

    def __buildLinkedGraph(self) -> Task:
        raise NotImplementedError

    def execute(self) -> None:
        raise NotImplementedError
