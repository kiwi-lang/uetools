from dataclasses import dataclass
from typing import Optional

from uetools.args.arguments import add_arguments
from uetools.args.command import Command, newparser
from uetools.core.conf import editor_commandlet, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter
from uetools.core.util import deduce_project


# fmt: off
@dataclass
class Arguments:
    project: Optional[str] = deduce_project()  # Name of the the project to open
    no_input: bool = True
# fmt: on


class ReSavePackages(Command):
    """Resave assets, fixing some issues that can arise when using marketplace assets

    Examples
    --------

    .. code-block:: console

       uecli gkscript RTSGame

    """

    name: str = "resavepackages"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, ReSavePackages)
        add_arguments(parser, Arguments)

    @staticmethod
    def execute(args):
        project = find_project(vars(args).pop("project"))

        cmd = editor_commandlet(project, "resavepackages") + [
            # "-VERIFY",
            # "-PACKAGEFOLDER="
        ]

        print(" ".join(cmd))
        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = ReSavePackages
