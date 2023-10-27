from dataclasses import dataclass
from typing import Optional

from argklass.command import Command

from uetools.core.conf import editor, find_project
from uetools.core.options import projectfield
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


class Open(Command):
    """Open the editor for a given project

    Examples
    --------

    .. code-block:: console

       uecli open RTSGameEditor

    """

    name: str = "open"

    @dataclass
    class Arguments:
        project: Optional[str] = projectfield()  # Name of the the project to open

    @staticmethod
    def execute(args):
        cmd = [editor()]

        if args.project:
            project = find_project(args.project)
            cmd.append(project)

        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = Open
