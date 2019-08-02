from pathlib import Path
import json

import toml

from borca.exceptions import InvalidTaskConfiguration


class Task:
    def __init__(self, task_data: dict) -> None:
        self.__verifyAndGatherData(task_data)

    def __verifyAndGatherData(self, data: dict) -> None:
        if 'name' not in data.keys():
            raise InvalidTaskConfiguration('All tasks must be named.')

        if type(data['name']) is not str:
            raise InvalidTaskConfiguration('All task names must be string type.')
        
        if data['name'] == '':
            raise InvalidTaskConfiguration('All task names must not be empty strings.')

        self.name = data['name']

        if 'commands' not in data.keys():
            raise InvalidTaskConfiguration('All tasks must have a "commands" field.')
        
        if type(data['commands']) is not list:
            raise InvalidTaskConfiguration('All task commands fields must be of type list.')
        
        self.__commands = []
        for command in data['commands']:
            if type(command) is not str:
                raise InvalidTaskConfiguration('All task command values must be of type string.')

            self.__commands.append(command)

        # optional items start here

        self.dependency_names = []
        if 'depends-on' in data.keys():
            if type(data['depends-on']) is not list:
                raise InvalidTaskConfiguration('All task dependencies must be in a list.')

            for dependency_name in data['depends-on']:
                if type(dependency_name) is not str:
                    raise InvalidTaskConfiguration('All task dependencies must be of type string.')

                self.__dependency_names.append(dependency_name)
            
        self.__input_paths = []
        if 'input-paths' in data.keys():
            if type(data['input-paths']) is not list:
                raise InvalidTaskConfiguration('All task input paths must be in a list.')

            for input_path in data['input-paths']:
                if type(input_path) is not str:
                    raise InvalidTaskConfiguration('All task input paths must be of type string.')

                self.__input_paths.append(input_path)

        self.__output_paths = []
        if 'output-paths' in data.keys():
            if type(data['output-paths']) is not list:
                raise InvalidTaskConfiguration('All task output paths must be in a list.')

            for input_path in data['output-paths']:
                if type(input_path) is not str:
                    raise InvalidTaskConfiguration('All task output paths must be of type string.')

                self.__output_paths.append(input_path)

    def execute(self) -> None:
        raise NotImplementedError
