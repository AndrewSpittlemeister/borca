from typing import Dict, Any, MutableMapping
import json

from borca.task import Task
from borca.util import createLogger
from borca.exceptions import InvalidToolConfiguration, InvalidTaskConfiguration


class BorcaDatagram:
    def __init__(self, config: Dict, toml_data: MutableMapping[str, Any]) -> None:
        self.__config = config
        self.__toml_data = toml_data
        self.__logger = createLogger('borca.parsing.BorcaDatagram', self.__config['verbosity'])

        self.__logger.debug(f"TOML as JSON:\n{json.dumps(self.__toml_data, indent=4)}")

        self.__default_task_name = self.__verifyAndGatherBorcaData()

        exit(0)  # FIXME: remove this later...

    def __verifyAndGatherBorcaData(self) -> str:
        '''Verifies that minimum information for the borca tool is present and is formatted correctly.'''

        if 'tool' not in self.__toml_data.keys():
            raise InvalidToolConfiguration('Heading for "tool" not found in pyproject.toml.')

        if 'borca' not in self.__toml_data['tool'].keys():
            raise InvalidToolConfiguration('Heading for "tool.borca" not found in pyproject.toml.')

        if 'default-task' not in self.__toml_data['tool']['borca'].keys():
            raise InvalidToolConfiguration('"default-task" field not found under the "tool.borca" heading.')

        if type(self.__toml_data['tool']['borca']['default-task']) is not str:
            raise InvalidToolConfiguration('Invalid type found for the "default-task" field (should be string).')

        if self.__toml_data['tool']['borca']['default-task'] == "":
            raise InvalidToolConfiguration('Invalid value for the "default-task" field (must not be empty).')

        self.__logger.debug(f"Borca data as JSON:\n{json.dumps(self.__toml_data['tool']['borca'], indent=4)}")

        return self.__toml_data['tool']['borca']['default-task']

    def getTaskMap(self) -> Dict[str, Task]:
        raise NotImplementedError
