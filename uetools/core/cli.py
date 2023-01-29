"""Entry point for the command line interface"""
from __future__ import annotations

from argparse import SUPPRESS, Action

import simple_parsing

from uetools.commands import commands, find_command
from uetools.core.conf import BadConfig, select_engine_version


# pylint: disable=protected-access
# pylint: disable=too-few-public-methods
class HelpFormatter(simple_parsing.SimpleHelpFormatter):
    """Tweak the arrgument usage format to not show too many duplicates"""

    def __init__(self, prog, max_help_position, width=None):
        super().__init__(prog=prog, max_help_position=max_help_position, width=width)
        self.command = find_command(prog.split(" ")[-1])

    def _get_help_string(self, action: Action) -> str | None:
        help = super()._get_help_string(action=action)
        lines = help.split("\n", maxsplit=1)
        return lines[0]

    def add_usage(self, usage, actions, groups, prefix=None):
        if usage is None and self.command:
            examples = "\n       ".join(self.command.examples())

            usage = examples + "\n\ndescription:\n    " + self.command.help()

        super().add_usage(usage, actions, groups, prefix)

    class _Section:
        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            """Format the help section"""

            offset = 0
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()

            join = self.formatter._join_parts

            frags = [func(*args) for func, args in self.items]

            item_help = join(frags[offset:])

            if self.parent is not None:
                self.formatter._dedent()

            # return nothing if the section was empty
            if not item_help:
                return ""

            # add the heading if the section was non-empty
            # pylint: disable=consider-using-f-string
            if self.heading is not SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                heading = "%*s%s:\n" % (current_indent, "", self.heading)
            else:
                heading = ""

            # join the section-initial newline, the heading and the help
            return join(["\n", heading, item_help, "\n"])


# pylint: disable=too-few-public-methods
class ArgumentParser(simple_parsing.ArgumentParser):
    """Force the argument parse to use the right formatter"""

    def _get_formatter(self):
        return HelpFormatter(prog=self.prog, max_help_position=45, width=None)
        # return BaseArgumentHelpFormatter()
        # return


def parse_args(argv):
    """Setup the argument parser for all supported commands"""
    parser = ArgumentParser()
    parser.add_argument(
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
    command = commands.get(cmd_name)

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
