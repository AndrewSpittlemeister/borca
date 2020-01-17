# borca

![](https://gitlab.com/AndrewSpittlemeister/borca/badges/master/pipeline.svg)

A PEP 518 compatible, explicit build orchestration tool for Python. It is a simple tool that allows for the creation of an acyclic-task graph made up of operations that use tools commonly found in a Python development stack (i.e. linting, testing, etc.). It makes no assumptions about its environment and does not attempt to modify it. Borca focuses on creating a model of a slim and extensible edition to the stock Python toolchain capabilities.