from argparse import ArgumentParser
from borca import Orchestrator


def main() -> None:
    parser = ArgumentParser(description="Python build orchestration tool.")

    parser.add_argument("task-name", nargs='?', help="name of the task to execute")
    parser.add_argument("--no-hash", action="store_true", help="does not use or generate task I/O hash")
    parser.add_argument(
        "--toml-path", type=str, default="pyproject.toml", help="specify alternate path to pyproject.toml file"
    )
    parser.add_argument(
        "--verbosity", type=int, default=1, choices=(0, 1, 2), help="specify verbosity 0, 1, or 2 (default 1)"
    )

    orchestrator = Orchestrator(vars(parser.parse_args()))
    orchestrator.run()


if __name__ == "__main__":
    main()
