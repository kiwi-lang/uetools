import os
from dataclasses import dataclass

from argklass.arguments import add_arguments
from argklass.command import Command, newparser

from uetools.core.conf import editor_commandlet, find_project
from uetools.core.run import popen_with_format
from uetools.core.util import command_builder
from uetools.format.base import Formatter


def fspath_to_unreal(project, path):
    if path is not None:
        path = path.replace("\\", "/")
        if path.startswith("/"):
            return path

    project_content = os.path.join(os.path.dirname(project), "Content")
    project_content = project_content.replace("\\", "/")

    if path is not None and path.startswith(project_content):
        return path.replace(project_content, "/Game").replace(".uasset", "")

    return path


class GKScript(Command):
    """Convert a Blueprint into GKScript"""

    # fmt: off
    @dataclass
    class Arguments:
        """Convert a Blueprint into GKScript

        Attributes
        ----------
        project: str
            Name of the project

        blueprint: str
            Name of the blueprint to convert

        Examples
        --------

        .. code-block:: console

        uecli gamekit gkscript RTSGame

        """

        project: str
        blueprint: str = None
        destination: str = None
        no_input: bool = True
    # fmt: on

    name: str = "gkscript"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, GKScript)
        add_arguments(parser, GKScript.Arguments)

    @staticmethod
    def execute(args):
        project = find_project(vars(args).pop("project"))

        args.blueprint = fspath_to_unreal(project, args.blueprint)
        cmd_args = command_builder(args)

        cmd = editor_commandlet(project, "GKScript", "-LogCmds=LogGKScript VeryVerbose") + cmd_args

        print(" ".join(cmd))

        fmt = Formatter()
        fmt.only.add("LogGKScript")
        return popen_with_format(fmt, cmd)


COMMANDS = GKScript
