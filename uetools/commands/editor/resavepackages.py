from dataclasses import dataclass
from typing import Optional

from argklass.command import Command

from uetools.core.conf import editor_commandlet, find_project
from uetools.core.options import projectfield
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter


class ReSavePackages(Command):
    """Resave assets, fixing some issues that can arise when using marketplace assets

    Examples
    --------

    .. code-block:: console

       uecli gkscript RTSGame

    """

    name: str = "resavepackages"

    # fmt: off
    @dataclass
    class Arguments:
        project: Optional[str] = projectfield()  # Name of the the project to open
        no_input: bool = True
    # fmt: on

    @staticmethod
    def execute(args):
        project = find_project(vars(args).pop("project"))

        cmd = (
            editor_commandlet(project, "resavepackages")
            + [
                # "-VERIFY",
                # "-PACKAGEFOLDER="
            ]
        )

        print(" ".join(cmd))
        fmt = Formatter()
        return popen_with_format(fmt, cmd)


COMMANDS = ReSavePackages
