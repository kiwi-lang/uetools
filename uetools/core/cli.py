"""Entry point for the command line interface"""
from __future__ import annotations

import argparse
from contextlib import contextmanager

from uetools.commands import discover_commands, command_cache_status

from .argformat import DumpParserAction, HelpAction, HelpActionException
from .command import ParentCommand
from .conf import BadConfig, select_engine_version
from .perf import show_timings, timeit


# Argument Parser cannot be pickled
def build_parser(commands):
    with timeit("build_parser"):
        parser = argparse.ArgumentParser(
            add_help=False, description="Unreal Engine Utility"
        )
        parser.add_argument(
            "-h", "--help", action=HelpAction, help="show this help message and exit"
        )
        parser.add_argument("-zyx", action=DumpParserAction, help="")
        parser.add_argument(
            "-v",
            "--engine-version",
            nargs="?",
            type=str,
            default=None,
            help="Engine version to use if you have multiple installed",
        )
        parser.add_argument(
            "-xyz",
            action="store_true",
            default=False,
            help="Show perf timing",
        )

        subparsers = parser.add_subparsers(dest="command")

        ParentCommand.dispatch = dict()
        for k, command in commands.items():
            with timeit(k):
                command.arguments(subparsers)

        return parser


def parse_args(commands, argv):
    """Setup the argument parser for all supported commands"""
    parser = build_parser(commands)

    with timeit("parse_args"):
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
    with timeit("discover_commands"):
        commands = discover_commands()

    with timeit("parse_args"):
        try:
            parsed_args = parse_args(commands, argv)
        except HelpActionException:
            
            msg = command_cache_status()
            if msg:
                print('\n')
                print(' ' * 10, 'NOTE: ', msg)
                print('\n')

            return 0
        except BadConfig:
            return -1

    cmd_name = parsed_args.command
    command = commands.get(cmd_name)

    if command is None:
        print(f"Action `{cmd_name}` not implemented")
        return -1

    with timeit("command.execute"):
        returncode = command.execute(parsed_args)

    if returncode is None:
        return 0

    return returncode


@contextmanager
def profiler(enabled=False):
    import io
    import pstats
    import cProfile

    with cProfile.Profile() as profile:
        profile.disable()
        if enabled:
            profile.enable()

        yield

        profile.disable()

        if enabled:
            s = io.StringIO()
            sortby = pstats.SortKey.CUMULATIVE
            ps = pstats.Stats(profile, stream=s).sort_stats(sortby)
            ps.print_stats(25)
            print(s.getvalue())


def main_force(argv=None):
    import sys

    with profiler("-xyz" in sys.argv):
        r = main()
    
    show_timings()
    sys.exit(r)


if __name__ == "__main__":
    main_force()
