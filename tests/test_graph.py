import pytest

import toml

from borca.parsing import Parser
from borca.exceptions import InvalidTaskgraph

def test_single():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

    assert task_names == ["build"]

def test_multiple_no_deps():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]

[[tool.borca.tasks]]
name = "lint"
commands = [
    "mypy borca",
    "black borca"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

    assert task_names == ["build"]

def test_multiple_partial_deps():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
depends_on = [
    "lint"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]

[[tool.borca.tasks]]
name = "lint"
commands = [
    "mypy borca",
    "black borca"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

    assert task_names == ["lint", "build"]

def test_multiple_linear_deps():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
depends_on = [
    "test"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
depends_on = [
    "lint"
]

[[tool.borca.tasks]]
name = "lint"
commands = [
    "mypy borca",
    "black borca"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

    assert task_names == ["lint", "test", "build"]

def test_diamond_dep_tree():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
depends_on = [
    "test",
    "security"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
depends_on = [
    "lint"
]

[[tool.borca.tasks]]
name = "security"
commands = [
    "bandit -r borca"
]
depends_on = [
    "lint"
]

[[tool.borca.tasks]]
name = "lint"
commands = [
    "mypy borca",
    "black borca"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

    assert (
        task_names == ["lint", "test", "security", "build"] or
        task_names == ["lint", "security", "test", "build"]
    )

def test_flux_dep_tree():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
depends_on = [
    "test"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
depends_on = [
    "lint",
    "security"
]

[[tool.borca.tasks]]
name = "security"
commands = [
    "bandit -r borca"
]

[[tool.borca.tasks]]
name = "lint"
commands = [
    "mypy borca",
    "black borca"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

    assert (
        task_names == ["security", "lint", "test", "build"] or
        task_names == ["lint", "security", "test", "build"]
    )

def test_redundant_dep_tree():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
depends_on = [
    "test",
    "security"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
depends_on = [
    "security"
]

[[tool.borca.tasks]]
name = "security"
commands = [
    "bandit -r borca"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

    assert task_names == ["security", "test", "build"]

def test_duplicate_dep_use():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
depends_on = [
    "test",
    "test"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

    assert task_names == ["test", "build"]

def test_circular_dep_tree():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
depends_on = [
    "test"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
depends_on = [
    "build"
]

'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    with pytest.raises(InvalidTaskgraph, match=r"Found circular dependency on task \".*\" to its dependency \".*\"") as e:
        task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]

def test_extended_circular_dep_tree():
    toml_text = \
'''
[tool.borca]
default_task = "build"

[[tool.borca.tasks]]
name = "build"
commands = [
    "poetry build --format wheel"
]
depends_on = [
    "test"
]

[[tool.borca.tasks]]
name = "test"
commands = [
    "pytest"
]
depends_on = [
    "lint"
]

[[tool.borca.tasks]]
name = "lint"
commands = [
    "mypy borca",
    "black borca"
]
depends_on = [
    "build"
]

'''
    config = {'task-name': 'build', 'no_hash': False, 'toml_path': 'pyproject.toml', 'verbosity': 2}
    toml_data = toml.loads(toml_text)
    with pytest.raises(InvalidTaskgraph, match=r"Found circular dependency on task \".*\" to its dependency \".*\"") as e:
        task_names = [task.name for task in Parser(config, toml_data).orderedTasks()]
