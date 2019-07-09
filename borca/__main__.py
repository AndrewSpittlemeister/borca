from argparse import ArgumentParser


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument("task", required=True, help="name of the task to execute")
    parser.add_argument("--no-hash", help="does not use or generate task I/O hash")
    parser.add_argument("--toml-path", help="specify alternate path to pyproject.toml file")
    parser.add_argument("--verbosity", help="specify verbosity 0, 1, or 2 (default 1)")

    args = parser.parse_args()
    print(args.echo)


if __name__ == "__main__":
    main()
