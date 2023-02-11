"""Entry point for the command line interface"""
from __future__ import annotations

import argparse

from uetools.commands import commands
from uetools.core.argformat import HelpAction
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
    import sys

    try:
        parsed_args = parse_args(argv)
    except BadConfig:
        sys.exit(-1)

    cmd_name = parsed_args.command
    print(cmd_name)
    command = commands.get(cmd_name)
    print(command)

    if command is None:
        print(f"Action `{cmd_name}` not implemented")
        return

    returncode = command.execute(parsed_args)

    if returncode is None:
        return

    if returncode != 0:
        sys.exit(returncode)


if __name__ == "__main__":
    main()
