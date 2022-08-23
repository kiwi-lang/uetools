from __future__ import annotations

from argparse import Namespace
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from typing import Dict, List


class Command:
    """Base class for all commands"""

    name: str
    help: str

    @staticmethod
    def arguments(subparsers):
        """Define the arguments of this command"""
        raise NotImplementedError()

    @staticmethod
    def execute(args):
        """Execute the command"""
        raise NotImplementedError()


def command_builder(args: Dict | Namespace) -> List[str]:
    """Convert a namespace of arguments into a list of command line arguments for unreal engine.
    Supports dataclasses (even nested) and custom command generation through the ``to_ue_cmd`` method.

    Examples
    --------

    >>> command_builder(dict(log=True, map='/Game/Map/TopDown'))
    ['-log', '-map=/Game/Map/TopDown']

    >>> @dataclass
    >>> class Arguments:
    ...     flag       : Optional[bool] = None
    ...     goalscore  : Optional[float] = None

    >>> command_builder(dict(vector=Arguments(flag=True, goalscore=2)))
    ['-flag', '-goalscore=2']

    >>> command_builder(dict(vector=Arguments(flag=False, goalscore=2)))
    ['-goalscore=2']


    >>> @dataclass
    >>> class Vector:
    ...     x: Optional[float] = 0
    ...     y: Optional[float] = 0
    ...     z: Optional[float] = 0
    ...     def to_ue_cmd(self, name, cmd):
    ...         cmd.append(f"-{name}=(X={self.x},Y={self.y},Z={self.z})")

    >>> command_builder(dict(vector=Vector(x=1, y=2, z=3)))
    ['-vector=(X=1,Y=2,Z=3)']


    """
    args = deepcopy(args)

    if isinstance(args, Namespace):
        args = vars(args)

    # Note: we do not NEED to pop them, UE ignore unknown arguments
    args.pop("command", None)
    args.pop("cli", None)
    args.pop("dry", None)

    cmd = []

    _command_builder(cmd, args)

    return cmd


def _command_builder(cmd, args):
    for k, v in args.items():
        if v is None:
            continue

        if isinstance(v, bool):
            if v is not None and v is True:
                cmd.append(f"-{k}")

        elif isinstance(v, (str, int)):
            cmd.append(f"-{k}={v}")

        elif hasattr(v, "to_ue_cmd"):
            v.to_ue_cmd(k, cmd)

        elif is_dataclass(v):
            _command_builder(cmd, asdict(v))
