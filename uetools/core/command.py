from __future__ import annotations

import os
from argparse import Namespace
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import asdict, is_dataclass

from uetools.core.argformat import HelpAction
from uetools.core.plugin import discover_plugins


def newparser(subparsers, commandcls: Command):
    """Add a subparser to the parser for the command"""
    # The help text is not showing :/
    line = commandcls.help().split("\n")[0]
    parser = subparsers.add_parser(
        commandcls.name, description=line, help=commandcls.help(), add_help=False
    )
    parser.add_argument(
        "-h", "--help", action=HelpAction, help="show this help message and exit"
    )
    return parser


@contextmanager
def chdir(root):
    """change directory and revert back to previous directory"""
    old = os.getcwd()
    os.chdir(root)

    yield
    os.chdir(old)


class Command:
    """Base class for all commands"""

    name: str

    @classmethod
    def help(cls) -> str:
        """Return the help text for the command"""
        return cls.__doc__ or ""

    @staticmethod
    def arguments(subparsers):
        """Define the arguments of this command"""
        raise NotImplementedError()

    @staticmethod
    def execute(args) -> int:
        """Execute the command"""
        raise NotImplementedError()

    @staticmethod
    def examples() -> list[str]:
        """returns a list of examples"""
        return []


def command_builder(args: dict | Namespace, ignore=None) -> list[str]:
    """Convert a namespace of arguments into a list of command line arguments for unreal engine.
    Supports dataclasses (even nested) and custom command generation through the ``to_ue_cmd`` method.

    Examples
    --------
    >>> from dataclasses import dataclass

    >>> command_builder(dict(log=True, map='/Game/Map/TopDown'))
    ['-log', '-map=/Game/Map/TopDown']

    >>> @dataclass
    ... class Arguments:
    ...     flag       : bool = False
    ...     goalscore  : Optional[float] = None
    ...     something  : Optional[str] = None

    >>> command_builder(dict(vector=Arguments(flag=True, goalscore=2, something=None)))
    ['-flag', '-goalscore=2']

    >>> command_builder(dict(vector=Arguments(flag=False, goalscore=2)))
    ['-goalscore=2']


    >>> @dataclass
    ... class Vector:
    ...     x: Optional[float] = 0
    ...     y: Optional[float] = 0
    ...     z: Optional[float] = 0
    ...     def to_ue_cmd(self, name, cmd):
    ...         cmd.append(f"-{name}=(X={self.x},Y={self.y},Z={self.z})")

    >>> command_builder(dict(vector=Vector(x=1, y=2, z=3)))
    ['-vector=(X=1,Y=2,Z=3)']

    >>> command_builder(Namespace(vector=Vector(x=1, y=2, z=3)))
    ['-vector=(X=1,Y=2,Z=3)']

    """
    if ignore is None:
        ignore = set()

    args = deepcopy(args)

    if isinstance(args, Namespace):
        args = vars(args)

    if not isinstance(args, dict):
        args = asdict(args)

    # Note: we do not NEED to pop them, UE ignore unknown arguments
    if isinstance(args, dict):
        args.pop("command", None)
        args.pop("cli", None)
        args.pop("dry", None)

    cmd = []

    _command_builder(cmd, args, ignore)

    return cmd


def _command_builder(cmd, args, ignore):
    for k, v in args.items():
        if v is None:
            continue

        if k in ignore:
            continue

        if isinstance(v, bool):
            if v is not None and v is True:
                cmd.append(f"-{k}")

        elif isinstance(v, (str, int)):
            cmd.append(f"-{k}={v}")

        elif hasattr(v, "to_ue_cmd"):
            v.to_ue_cmd(k, cmd)

        elif is_dataclass(v):
            _command_builder(cmd, asdict(v), ignore)


class ParentCommand(Command):
    """Loads child module as subcommands"""

    dispatch: dict = dict()

    @staticmethod
    def module():
        return None

    @classmethod
    def arguments(cls, subparsers):
        parser = newparser(subparsers, cls)
        subsubparsers = parser.add_subparsers(dest="subcommand", help=cls.help())

        for _, module in discover_plugins(cls.module()).items():
            if hasattr(module, "COMMANDS"):
                commands = getattr(module, "COMMANDS")

                if not isinstance(commands, list):
                    commands = [commands]

                for cmd in commands:
                    cmd.arguments(subsubparsers)
                    cls.dispatch[cmd.name] = cmd

    @classmethod
    def execute(cls, args):
        subcmd = vars(args).pop("subcommand")

        cmd = cls.dispatch.get(subcmd, None)
        if cmd:
            cmd.execute(args)
            return

        raise RuntimeError(f"Subcommand {cls.name} {subcmd} is not defined")
