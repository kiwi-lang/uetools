from dataclasses import dataclass

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


class ReSavePackages(Command):
    """Resave assets, fixing some issues that can arise when using marketplace assets"""

    name: str = "resavepackages"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, ReSavePackages)
        parser.add_arguments(Arguments, dest="args")

    @staticmethod
    def execute(args):
        args = args.args
        project = find_project(args.project)

        cmd = editor_commandlet(project, "resavepackages") + [
            # "-VERIFY",
            # "-PACKAGEFOLDER="
        ]

        print(" ".join(cmd))
        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = ReSavePackages
