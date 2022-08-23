"""Entry point for the command line interface"""
from __future__ import annotations

from argparse import SUPPRESS

import simple_parsing

from uetools.commands import commands


# pylint: disable=protected-access
# pylint: disable=too-few-public-methods
class HelpFormatter(simple_parsing.SimpleHelpFormatter):
    """Tweak the arrgument usage format to not show too many duplicates"""

    class _Section:
        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            """Format the help section"""
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()

                # skip the first item which is a giga dump of all the arguments we already know about
                # the function is _format_action
                self.items = self.items[1:]

            join = self.formatter._join_parts

            item_help = join([func(*args) for func, args in self.items])

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
