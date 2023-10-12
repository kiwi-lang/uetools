import argparse
import textwrap
from typing import Any


class ArgumentFormaterBase:
    def __init__(self) -> None:
        self.group_increase_indent = False
        self.show_groups = True
        self.newline_between_groups = False
        self.depth_limit = 0
        self.col = 50
        self.acc = []

    def column(self, depth):
        return self.col - depth * 2

    def show(self):
        for arg, kwargs in self.acc:
            print(*arg, **kwargs)
        self.acc = []

    def __call__(self, parser: argparse.ArgumentParser, depth: int = 0) -> Any:
        if self.group_increase_indent and self.show_groups:
            depth += 1

        if self.depth_limit > 0 and depth > self.depth_limit:
            return

        if depth == 0:
            self.print()
            self.print(f"{'  ' * (depth + 1)} {parser.description}")
            self.print()
            self.print(f"{'  ' * (depth + 2)} {parser.format_usage()}")

        for group in parser._action_groups:
            self.format_group(group, depth)

            for action in group._group_actions:
                if isinstance(action, argparse._SubParsersAction):
                    choices = action.choices

                    for name, choice in choices.items():
                        self.format_action(action, depth + 1, name=name)
                        self(choice, depth + 2)
                else:
                    self.format_action(action, depth + 1)

            if self.newline_between_groups:
                self.print()

    def print(self, *args, **kwargs):
        self.acc.append((args, kwargs))

    def format_group(self, group: argparse._ArgumentGroup, depth: int):
        if not self.show_groups:
            return

        if group._group_actions:
            line = f"{'  ' * (depth - 1)} {group.title:<{self.column(depth - 1)}} {type(group).__name__}"
            self.print(line)

    def format_action(self, action: argparse.Action, depth: int, name=None):
        name = name or action.dest

        line = f"{'  ' * depth} {name:<{self.column(depth)}} {type(action).__name__}"
        self.print(line)


class ArgumentFormater(ArgumentFormaterBase):
    def __init__(self) -> None:
        super().__init__()
        self.printed_help = False
        self.description_width = 80

    def format_group(self, group: argparse._ArgumentGroup, depth: int):
        if not self.show_groups:
            return

        if depth > 0:
            return

        def count_action(actions):
            acc = 0
            for action in actions:
                if isinstance(action, (argparse._HelpAction, HelpAction)):
                    continue
                acc += 1
            return acc

        if count_action(group._group_actions) > 0:
            line = f"\n{group.title:<{self.column(0)}}{group.description or ''}"
            self.print(line)

    def format_action(self, action: argparse.Action, depth: int, name=None):
        """Format an argparse action"""
        indent = "  " * depth

        # Ignore help
        if isinstance(action, argparse._HelpAction):
            if not self.printed_help:
                self.print(f"{indent}{'-h, --help':<{self.column(depth)}} Show help")
                self.printed_help = True
            return

        # Subparser
        if name is not None and (parser := action.choices[name]):
            title = name
            if parser.description is not None:
                title = parser.description.partition("\n")[0]
            self.print(f"{indent}{name:<{self.column(depth)}} {title}")
            return

        names = action.dest
        if action.option_strings:
            names = ", ".join(action.option_strings)

        type = ""
        if action.type:
            type = f": {action.type.__name__}"

        if isinstance(action, (argparse._StoreTrueAction, argparse._StoreFalseAction)):
            type = ": bool"

        if action.nargs and action.nargs != 0:
            type += str(action.nargs)

        default = ""
        if action.default is not None:
            default = " = " + str(action.default)

        help = ""
        if action.help:
            help = action.help

        show_options = False
        choices = action.choices
        if choices is not None:
            choices = f'Options: {", ".join(choices)}'
            show_options = True

        if not help and choices is not None:
            show_options = False
            help = choices

        def show_line(arg, help):
            if help is None or help == "":
                self.print(f"{indent}{arg:<{self.column(depth)}} {help}")
                return

            wrap_iter = textwrap.wrap(
                help, width=self.description_width, subsequent_indent=" "
            )

            for i, line in enumerate(wrap_iter):
                if i == 0:
                    self.print(f"{indent}{arg:<{self.column(depth)}} {line}")
                else:
                    self.print(f"{indent}{' ':<{self.column(depth)}} {line}")

        #
        arg = f"{names}{type}{default}"
        show_line(arg, help)
        if show_options:
            show_line("", choices)


def show_parsing_tree(parser: argparse.ArgumentParser, depth: int = 0):
    format = ArgumentFormaterBase()
    format(parser, depth)
    format.show()


def recursively_show_actions(parser: argparse.ArgumentParser, depth: int = 0):
    fmt = ArgumentFormater()
    fmt.depth_limit = 2
    fmt(parser, 0)
    fmt.show()


class HelpActionException(Exception):
    pass


class HelpAction(argparse._HelpAction):
    def __init__(self, *args, docstring=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.docstring = docstring

    def __call__(self, parser, namespace, values, option_string=None):
        recursively_show_actions(parser)
        raise HelpActionException()


class DumpParserAction(argparse._HelpAction):
    def __init__(self, *args, docstring=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.docstring = docstring

    def __call__(self, parser, namespace, values, option_string=None):
        show_parsing_tree(parser)
        parser.exit()


def normalize(namespace):
    new = argparse.Namespace()
    for k, v in vars(namespace).items():
        current = new
        keys = k.split(".")

        for k in keys[:-1]:
            if k in current:
                current = getattr(current, k)
            else:
                next = argparse.Namespace()
                setattr(current, k, next)
                current = next

        setattr(current, keys[-1], v)
    return new
