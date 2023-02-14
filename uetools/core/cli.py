"""Entry point for the command line interface"""
from __future__ import annotations

import argparse

from uetools.commands import commands
from uetools.core.argformat import HelpAction
from uetools.core.command import ParentCommand
from uetools.core.conf import BadConfig, select_engine_version


def parse_args(argv):
    """Setup the argument parser for all supported commands"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-h", "--help", action=HelpAction, help="show this help message and exit"
    )
    parser.add_argument(
        "-v",
        "--engine-version",
        nargs="?",
        type=str,
        default=None,
        help="Engine version to use if you have multiple installed",
    )

    subparsers = parser.add_subparsers(dest="command")

    ParentCommand.dispatch = dict()
    for _, command in commands.items():
        command.arguments(subparsers)

    args = parser.parse_args(argv)

    if args.engine_version is not None:
        select_engine_version(args.engine_version)
        args.engine_version = None

    return args


def args(*a):
    """Utility to turn arguments into a list"""
    return a


def main(argv=None):
    """Entry point for the command line interface"""
    try:
        parsed_args = parse_args(argv)
    except BadConfig:
        return -1

    cmd_name = parsed_args.command
    command = commands.get(cmd_name)

    if command is None:
        print(f"Action `{cmd_name}` not implemented")
        return -1

    returncode = command.execute(parsed_args)

    if returncode is None:
        return 0

    return returncode


def main_force(argv=None):
    import sys

    sys.exit(main())


if __name__ == "__main__":
    main_force()
