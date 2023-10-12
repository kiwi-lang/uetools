from dataclasses import dataclass
from typing import Optional

from uetools.args.arguments import add_arguments
from uetools.args.command import Command, newparser
from uetools.core.conf import editor, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


@dataclass
class Arguments:
    project: Optional[str] = None  # Name of the the project to open


class Open(Command):
    """Open the editor for a given project

    Examples
    --------

    .. code-block:: console

       uecli open RTSGameEditor

    """

    name: str = "open"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Open)
        add_arguments(parser, Arguments)

    @staticmethod
    def execute(args):
        cmd = [editor()]

        if args.project:
            project = find_project(args.project)
            cmd.append(project)

        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = Open
