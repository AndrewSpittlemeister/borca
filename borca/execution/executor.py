from typing import List, Dict, Tuple, Union
from pathlib import Path
from hashlib import md5
import subprocess  # nosec

from borca.util import createLogger
from borca.exceptions import BorcaException
from borca.parsing import Task


class Executor:
    def __init__(self, config: Dict, tasks: List[Task]) -> None:
        self.__config = config
        self.__tasks = tasks
        self.__logger = createLogger('borca.execution.Executor', self.__config['verbosity'])
        self.__root_path = Path(self.__config["toml_path"]).resolve().parent
        self.__cache_directory = Path(f"{self.__root_path}/.borca_cache").resolve()

    def run(self) -> Tuple[int, int, int]:
        completed_tasks: int = 0
        cached_tasks: int = 0
        check_cache = True

        if not self.__config["no_hash"]:
            cached_project_hash_in, cached_project_hash_out = self.__getCachedTaskHash("project")

            try:
                current_project_hash_in, current_project_hash_out = self.__getCurrentTaskHash(
                    "project", [self.__config["toml_path"]], []
                )

                check_cache = (
                    cached_project_hash_in == current_project_hash_in
                    and cached_project_hash_out == current_project_hash_out
                )

                if check_cache:
                    self.__logger.info("Caching enabled for this execution.")
                else:
                    self.__logger.info(
                        "Detected change in config file, therefore task caches will not be used, only updated."
                    )

                self.__cacheTask("project", current_project_hash_in, current_project_hash_out)

            except BorcaException as e:
                self.__logger.warn(
                    f"Unable to calculate hash for the project config, task caches will not be used, only updated."
                )

        else:
            self.__logger.info("Caching will neither be used or updated.")

        for task in self.__tasks:
            if (not self.__config["no_hash"]) and (len(task.input_paths) + len(task.output_paths) > 0):

                try:
                    current_task_hash_in, current_task_hash_out = self.__getCurrentTaskHash(
                        task.name, task.input_paths, task.output_paths
                    )

                    if check_cache:
                        cached_task_hash_in, cached_task_hash_out = self.__getCachedTaskHash(task.name)

                        if (
                            cached_task_hash_in == current_task_hash_in
                            and cached_task_hash_out == current_task_hash_out
                        ):
                            self.__logger.info(f"Task {task.name} is up-to-date")
                            cached_tasks += 1
                            continue

                except BorcaException as e:
                    self.__logger.warn(f"{e}")

            self.__logger.info(f"Executing task: {task.name}")

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

            if (not self.__config["no_hash"]) and (len(task.input_paths) + len(task.output_paths) > 0):

                try:
                    current_task_hash_in, current_task_hash_out = self.__getCurrentTaskHash(
                        task.name, task.input_paths, task.output_paths
                    )
                    self.__cacheTask(task.name, current_task_hash_in, current_task_hash_out)

                except BorcaException as e:
                    self.__logger.warn(f"{e}")

        return len(self.__tasks), completed_tasks, cached_tasks

    def __getCachedTaskHash(self, task_name: str) -> Tuple[bytes, bytes]:
        '''
            Will attempt to gather input and output hashes for a given task name, will default to an empty
                byte string if it failed for any reason, insinuating that it does not exist yet or may never.
        '''
        input_cache_file = Path(f"{self.__cache_directory}/{task_name}.in").resolve()
        try:
            input_cache = input_cache_file.read_bytes()
        except:
            # pretend that it doesn't exist for now
            input_cache = b""

        output_cache_file = Path(f"{self.__cache_directory}/{task_name}.out").resolve()
        try:
            output_cache = output_cache_file.read_bytes()
        except:
            # pretend that it doesn't exist for now
            output_cache = b""

        return input_cache, output_cache

    def __getCurrentTaskHash(
        self, task_name: str, input_patterns: List[str], output_patterns: List[str]
    ) -> Tuple[bytes, bytes]:
        '''
            Will produce has byte strings for both input and output patterns. These byte strings will default to an
                empty byte string when no patterns are specified and will throw an error when the all files of valid 
                patterns fail to be hashed. 
        '''

        input_hash = md5()  # nosec
        if len(input_patterns) > 0:
            for pattern in input_patterns:
                for path in Path(".").glob(pattern):
                    path = path.resolve()
                    if path.exists() and path.is_file():  # NOTE: this will disregard directory only paths
                        try:
                            input_hash.update(path.read_bytes())
                        except:
                            raise BorcaException(
                                f"Unable to compute output hash for {path} on task {task_name}, caching for this task will be disabled."
                            )
                    else:
                        self.__logger.warn(f"Input path {path} on task {task_name} is not a valid file.")
                        # but allow other paths to create a hash

            input_hash_bytes = input_hash.digest()
        else:
            input_hash_bytes = b""

        output_hash = md5()  # nosec
        if len(output_patterns) > 0:
            for pattern in output_patterns:
                for path in Path(".").glob(pattern):
                    path = path.resolve()
                    if path.exists() and path.is_file():  # NOTE: this will disregard directory only paths
                        try:
                            output_hash.update(path.read_bytes())
                        except:
                            raise BorcaException(
                                f"Unable to compute output hash for {path} on task {task_name}, caching for this task will be disabled."
                            )
                    else:
                        self.__logger.warn(f"Input path {path} on task {task_name} is not valid.")
                        # but allow other paths to create a hash

            output_hash_bytes = output_hash.digest()
        else:
            output_hash_bytes = b""

        return input_hash_bytes, output_hash_bytes

    def __cacheTask(self, task_name, input_hash: bytes, output_hash: bytes) -> None:
        if type(input_hash) is bytes:
            input_cache_file = Path(f"{self.__cache_directory}/{task_name}.in").resolve()
            input_cache_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                input_cache_file.write_bytes(input_hash)
            except Exception as e:
                self.__logger.warn(f"Unable to update input cache for task: {task_name}")

        if type(output_hash) is bytes:
            output_cache_file = Path(f"{self.__cache_directory}/{task_name}.out").resolve()
            output_cache_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                output_cache_file.write_bytes(output_hash)
            except Exception as e:
                self.__logger.warn(f"Unable to update output cache for task: {task_name}")
