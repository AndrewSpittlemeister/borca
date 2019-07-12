from typing import List, Dict
from queue import SimpleQueue as Queue

from borca.task import Task
from borca.util import createLogger


class TaskGraph:
    def __init__(self, config: Dict, tasks: List[Task]) -> None:
        self.__config = config
        self.__taskList = tasks
        self.__logger = createLogger('borca.TaskGraph', self.__config['verbosity'])

        self.__root = self.__buildLinkedGraph()
        self.__logger.info('Successfully constructed acyclic task graph.')

        self.__queue = self.__buildTaskQueue()
        self.__logger.info('Successfully constructed task queue.')

    def __buildLinkedGraph(self) -> Task:
        raise NotImplementedError

    def __buildTaskQueue(self) -> Queue:
        raise NotImplementedError

    def execute(self) -> None:
        while not self.__queue.empty():
            self.__queue.get().execute()
