from typing import Dict, Any, List, MutableMapping
import json

from pydantic import BaseModel as PydanticBaseModel

from borca.parsing import Task, BorcaData
from borca.util import createLogger
from borca.exceptions import InvalidToolConfiguration, InvalidTaskgraph


class Parser:
    def __init__(self, config: Dict, toml_data: MutableMapping[str, Any]) -> None:
        self.__logger = createLogger('borca.parsing.Parser', config['verbosity'])
        self.__config = config
        self.__toml_data = toml_data

        if 'tool' not in self.__toml_data.keys():
            raise InvalidToolConfiguration('Heading for "tool" not found in pyproject.toml.')

        if 'borca' not in self.__toml_data['tool'].keys():
            raise InvalidToolConfiguration('Heading for "tool.borca" not found in pyproject.toml.')

        if type(self.__toml_data['tool']['borca']) is not dict:
            raise InvalidToolConfiguration(
                f"Invalid value for the tool.borca field (must be a dictionary but found {type(self.__toml_data['tool']['borca'])})"
            )

        self.__data = BorcaData(**self.__toml_data['tool']['borca'])

        self.__root_task_name = self.__verifyTaskCollection()
        self.__ordered_tasks = self.__buildTaskOrder()

    def __verifyTaskCollection(self) -> str:
        names = set([task.name for task in self.__data.tasks])

        if len(names) != len(self.__data.tasks):
            raise InvalidToolConfiguration('Found multiple tasks with the same name.')

        root = self.__config.get("task-name")
        if root is None:
            root = self.__data.default_task
            self.__logger.info(f"Using default task: {self.__data.default_task}")

        if root not in names:
            raise InvalidToolConfiguration('Default or specified task name was not found in defined tasks.')

        return root

    def __buildTaskOrder(self) -> List[Task]:

        # build {name : Task} map
        task_map: Dict[str, Task] = {}
        for task in self.__data.tasks:
            task_map[task.name] = task

        # add dependents to each task
        for task in self.__data.tasks:
            for dep_name in task.depends_on:
                task.dependencies.add(task_map[dep_name])

        def build(task: Task, visited: List[Task] = [], ordered: List[Task] = []) -> List[Task]:

            # print(f"looking at task {task.name}")

            # Handle leaf node tasks
            if len(task.dependencies) == 0:
                if task not in ordered:
                    # print(f"adding task {task.name}")
                    ordered.append(task)

            # Handle tasks with dependencies
            else:
                for dep in task.dependencies:
                    if dep in visited:
                        raise InvalidTaskgraph(
                            f'Found circular dependency on task "{task.name}" to its dependency "{dep.name}"'
                        )

                    visited.append(task)
                    build(dep, visited)
                    visited.pop()

                if task not in ordered:
                    # print(f"adding task from else {task.name}")
                    ordered.append(task)

            return ordered

        ordered = build(task_map[self.__root_task_name])

        self.__logger.debug(f"Task Order: {[task.name for task in ordered]}")

        return ordered

    def orderedTasks(self) -> List[Task]:
        return self.__ordered_tasks.copy()
