import argparse


def recursively_show_actions(parser: argparse.ArgumentParser):
    if parser.description:
        print(parser.description)

    _recursively_show_actions(parser, 2)


def _recursively_show_actions(parser: argparse.ArgumentParser, depth: int = 0):
    for group in parser._action_groups:
        format_group(group, depth)


def format_group(group: argparse._ArgumentGroup, depth: int):
    indent = "  " * depth

    if group._group_actions and depth <= 2:
        print()
        print(f"{group.title}")

    for action in group._group_actions:
        if isinstance(action, argparse._SubParsersAction):
            choices = action.choices

            for name, choice in choices.items():
                title = choice.description.partition("\n")[0]
                if isinstance(choice, argparse.ArgumentParser):
                    print(f"{indent}{name:<40} {title}")
                    _recursively_show_actions(choice, depth + 1)
        else:
            format_action(action, depth)


def format_action(action: argparse.Action, depth: int):
    """Format an argparse action"""
    indent = "  " * depth

    if depth > 2:
        return

    if isinstance(action, argparse._HelpAction):
        return

    # print(f'{indent}{action}')

    names = action.dest
    if action.option_strings:
        names = ", ".join(action.option_strings)

    type = ""
    if action.type:
        type = f": {action.type.__name__}"

    if isinstance(action, argparse._StoreTrueAction):
        type = ": bool"

    if action.nargs and action.nargs != 0:
        type += str(action.nargs)

    default = ""
    if action.default is not None:
        default = " = " + str(action.default)

    help = ""
    if action.help:
        help = action.help

    arg = f"{names}{type}{default}"
    print(f"{indent}{arg:<40} {help}")

    choices = action.choices
    if choices is not None:
        print(f'{indent}{"":<40}   Options: ({", ".join(choices)})')


class HelpAction(argparse._HelpAction):
    def __init__(self, *args, docstring=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.docstring = docstring

    def __call__(self, parser, namespace, values, option_string=None):
        recursively_show_actions(parser)
        parser.exit()
