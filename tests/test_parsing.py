import pytest

import toml
import pydantic

from borca.parsing import Parser
from borca.exceptions import InvalidToolConfiguration

def test_missing_tasks():
    toml_text = \
'''
[tool.borca]
default_task = "build"
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)

def test_missing_default_definition():
    toml_text = \
'''
[tool.borca]

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)

def test_bad_task_heading_format():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[tool.borca.tasks]
name = "build"
commands = [
    "poetry build --format wheel"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)

def test_missing_default_task():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(InvalidToolConfiguration) as e:
        parser = Parser(config, toml_data)

def test_bad_borca_pathing():
    toml_text = \
'''
[tool.borc]
default_task = "build"

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)

def test_bad_task_pathing():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.task]]
name = "test"
commands = [
    "pytest"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)

def test_bad_tool_pathing():
    toml_text = \
'''
[tol.borca]
default_task = "test"

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)

def test_missing_task_name():
    toml_text = \
'''
[tool.borca]
default_task = "test"

[[tool.borca.tasks]]
commands = [
    "pytest"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)

def test_missing_task_commands():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)

def test_bad_task_commands_format():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = "poetry build --format wheel"
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 1}
    toml_data = toml.loads(toml_text)
    with pytest.raises(pydantic.error_wrappers.ValidationError) as e:
        parser = Parser(config, toml_data)
