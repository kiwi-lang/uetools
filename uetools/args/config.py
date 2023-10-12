import argparse
from typing import Any

import hjson

from .group import _getattr
from .argformat import ArgumentFormaterBase


class ArgumentConfig(ArgumentFormaterBase):
    """Traverse the argumentparser tree and save or load a configuration"""

    def __init__(self, config, args=None):
        super().__init__()

        self.args = args
        self.root = config
        self.stack = [(self.root, None, args)]

        self.group_by_parser = True
        self.group_by_dataclass = True
        self.ignore_default = True
        self.ignore_single_group = False
        self.remove_empty = True
        self.eager = False

        self.ignore_groups = {
            "positional arguments",
            "optional arguments",
            # "Arguments"
        }

    @property
    def current(self):
        return self.stack[-1][0]

    @property
    def arggroup(self):
        return self.stack[-1][2]

    @property
    def actionkey(self):
        keys = []
        for _, k in self.stack[1:]:
            keys.append(k)
        return ".".join(keys)

    def new_group(self, name):
        newgroup = self.current.get(name, dict())
        arggroup = _getattr(self.arggroup, name, self.arggroup)

        self.current[name] = newgroup
        self.stack.append((newgroup, name, arggroup))

    def pop_group(self):
        group, name, _ = self.stack.pop()
        self.current[name] = group

        if self.remove_empty and len(group) == 0:
            self.current.pop(name)

    def __call__(self, parser: argparse.ArgumentParser, depth: int = 0) -> Any:
        n = len(parser._action_groups)
        skip_group = self.ignore_single_group and n == 1

        for group in parser._action_groups:
            should_make_group = (
                isinstance(group, argparse._ArgumentGroup)
                and group.title not in self.ignore_groups  # Argument Group
                and self.group_by_dataclass  # Not ignored  # We want to group our output as well
            )
            make_group = (not skip_group) and should_make_group

            if make_group:
                dest = _getattr(group, "_dest", group.title)
                assert dest is not None
                self.new_group(dest)

            self.format_group(group, depth)

            if make_group:
                self.pop_group()

    def format_group(self, group: argparse._ArgumentGroup, depth: int):
        for action in group._group_actions:
            if isinstance(action, argparse._SubParsersAction):
                self.format_subparser(action, depth)
            else:
                self.format_action(action, depth + 1)

    def format_subparser(self, action: argparse._SubParsersAction, depth: int):
        # Get selected command from the configuration
        selected = self.current.get(action.dest)

        if self.args is not None:
            # Selected command from command line
            selected = _getattr(self.arggroup, action.dest, selected)  #  #  #

            # update selection
            self.current[action.dest] = selected
            vars(self.arggroup)[action.dest] = selected

        for name, choice in action.choices.items():

            if self.group_by_parser:
                self.new_group(name)

            if self.eager or selected == name:
                self(choice, depth + 2)

            if self.group_by_parser:
                self.pop_group()

        return True

    def format_action(self, action: argparse.Action, depth: int, name=None):
        name = name or action.dest

        if action.default != argparse.SUPPRESS:
            # Hardcoded Default
            value1 = action.default

            # Fetch the value inside the config
            value2 = self.current.get(name)

            # Overriden default in commandline
            value3 = _getattr(self.arggroup, name, None)

            value = value3 or value2 or value1

            # Update config with latest value
            if not self.ignore_default or value != action.default:
                self.current[name] = value

            action.default = value

            # Update the arguments
            vars(self.arggroup)[name] = value


def apply_defaults(parser, configfile, cls=ArgumentConfig):
    with open(configfile, "r") as fp:
        config = hjson.load(fp)

    transform = cls(config)
    transform(parser)
    return parser


def save_defaults(parser, configfile, cls=ArgumentConfig):
    defaults = dict()

    transform = cls(defaults)
    transform(parser)

    with open(configfile, "w") as fp:
        hjson.dump(defaults, fp)


def apply_config(parser, args, configfile, cls=ArgumentConfig):
    with open(configfile, "r") as fp:
        config = hjson.load(fp)

    transform = cls(config, args)
    transform(parser)


def save_as_config(parser, args, configfile, cls=ArgumentConfig):
    defaults = dict()

    transform = cls(defaults, args)
    transform(parser)

    with open(configfile, "w") as fp:
        hjson.dump(defaults, fp)
