from dataclasses import dataclass

from uetools.core.arguments import add_arguments
from uetools.core.command import Command, newparser
from uetools.core.conf import editor_commandlet, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


# fmt: off
@dataclass
class Arguments:
    """Convert a Blueprint into GKScript

    Attributes
    ----------
    project: str
        Name of the project

    Examples
    --------

    .. code-block:: console

       uecli gkscript RTSGame

    """

    project: str
    no_input: bool = True


# fmt: on


class GKScript(Command):
    """Convert a Blueprint into GKScript"""

    name: str = "gkscript"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, GKScript)
        add_arguments(parser, Arguments)

    @staticmethod
    def execute(args):
        project = find_project(args.project)

        cmd = editor_commandlet(project, "GKScript") + [
            # Arguments
        ]
        print(" ".join(cmd))

        fmt = Formatter()
        fmt.only.add("LogGKScript")
        return popen_with_format(fmt, cmd)


COMMANDS = GKScript
