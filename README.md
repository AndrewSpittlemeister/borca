# borca

![pipeline](https://gitlab.com/AndrewSpittlemeister/borca/badges/master/pipeline.svg)

A PEP 518 compatible, explicit build orchestration (*"borca"*, it's a stretch; I know) tool for Python. It is a simple tool that allows for the creation of an acyclic-task graph made up of custom operations that are typically using tools commonly found in a Python development stack (i.e. linting, testing, etc.). It makes no assumptions about its environment and does not attempt to modify it. Borca focuses on creating a model of a slim and extensible edition to the stock Python toolchain capabilities.

## Current Condition
- [x] Acyclic task graph generation
- [x] Define default task
- [x] Optionally define custom `.toml` file path
- [ ] Incremental builds with task state caching

## Installation
Recommended installation is with `pip`:
```
pip install borca
```

Or even better, add it to the developer dependencies in your `pyproject.toml` file.

## Example Usage
Borca actually uses borca itself, so take a look at its own [pyproject.toml](https://gitlab.com/AndrewSpittlemeister/borca/blob/master/pyproject.toml) file and take a look at how it is structured. I generally use borca in the context of a virtual environment management tool such as `poetry` or `flit`.

```
$ poetry run borca test
```
This can get a little weird when defining a build task where you want to use something like the `poetry` build command (as borca does on itself) because it will create a nested virtual environment when invoking the `poetry` command again. While weird, this doesn't generally create any problems.

Although, this is not necessary if you wish to install borca manually.
```
$ borca test
```

General usage of the borca cli is as follows:
```
usage: borca [-h] [--no-hash] [--toml-path TOML_PATH] [--verbosity {0,1,2}] task-name

Python build orchestration tool.

positional arguments:
  task-name             name of the task to execute

optional arguments:
  -h, --help            show this help message and exit
  --no-hash             does not use or generate task I/O hash
  --toml-path TOML_PATH
                        specify alternate path to pyproject.toml file
  --verbosity {0,1,2}   specify verbosity 0, 1, or 2 (default 1)
```

## Note on Development Process
This is a tool I made primarily for myself; and as you can probably see from the commit history, I don't work on it very often. I work as a full-time software engineer and am getting my Master's in CS at the same time as well, so I don't find myself devoting a lot of time to side projects. That being said, feel free post issues or merge requests on GitLab. On that note, if you are seeing this on GitHub, be aware that development for this is actually done on GitLab due to its dope CI/CD features.