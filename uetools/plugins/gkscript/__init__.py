from dataclasses import dataclass

from uetools.core.command import Command, newparser
from uetools.core.conf import find_project, editor_cmd
from uetools.format.base import Formatter
from uetools.core.run import popen_with_format

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
        parser.add_arguments(Arguments, dest="gkscript")

    @staticmethod
    def execute(args):
        args = args.gkscript
        project = find_project(args.project)

        cmd = editor_commandlet(project, "GKScript") + [
            # Arguments
        ]
        print(" ".join(cmd))

        fmt = Formatter()
        fmt.only.add('LogGKScript')
        return popen_with_format(fmt, cmd)

COMMANDS = GKScript
