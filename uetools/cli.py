"""Entry point for the command line interface"""
from argparse import ArgumentParser

from uetools.commands import commands


def parse_args():
    """Setup the argument parser for all supported commands"""
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    for _, command in commands.items():
        command.arguments(subparsers)

    return parser.parse_args()


def main():
    """Entry point for the command line interface"""
    args = parse_args()

    cmd_name = args.command
    command = commands.get(cmd_name)

    if command is None:
        print(f"Action `{cmd_name}` not implemented")
        return

    command.execute(args)


if __name__ == "__main__":
    main()
