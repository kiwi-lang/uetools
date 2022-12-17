import os
from dataclasses import dataclass

import pkg_resources

from uetools.core.command import Command, newparser
from uetools.core.conf import find_project


@dataclass
class Arguments:
    """Create a dedicated server target for a given project

    Attributes
    ----------
    project: str
        Name of the project to add the server target

    Examples
    --------

    .. code-block:: console

       # Add the new server target
       uecli dedicated RTSGame

       # update visual studio project
       uecli regenerate RTSGame

       # Build the new target
       uecli build RTSGameServer

    """

    project: str


class Dedicated(Command):
    """Create a dedicated server target for a given project"""

    name: str = "dedicated"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Dedicated)
        parser.add_argument(
            "project", default=None, type=str, help="name of your project"
        )

    @staticmethod
    def execute(args):
        project = find_project(args.project)
        folder = os.path.dirname(project)

        source_folder = os.path.join(folder, "Source")
        server_target = os.path.join(source_folder, f"{args.project}Server.Target.cs")

        if os.path.exists(server_target):
            print(f"{server_target} already exists")
            return 0

        Dedicated.generate_server_target(args.project, server_target)

        return 0

    @staticmethod
    def generate_server_target(project, server_target):
        """Add the UBT server target to a given project"""
        template = pkg_resources.resource_filename(
            __name__, "../templates/TemplateServer.Target"
        )

        with open(template, "r", encoding="utf-8") as template_file:
            template = template_file.read()

        template = template.replace("{ProjectName}", project)

        with open(server_target, "w", encoding="utf-8") as file:
            file.write(template)


COMMANDS = Dedicated
