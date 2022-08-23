import os
from dataclasses import dataclass

import pkg_resources

from uetools.command import Command
from uetools.conf import load_conf


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

       # Build the new target
       uecli build RTSGameServer

    """

    project: str


class Dedicated(Command):
    """Create a dedicated server target for a given project"""

    name: str = "dedicated"

    @staticmethod
    def arguments(subparsers):
        init = subparsers.add_parser(
            Dedicated.name, help="Create a dedicated server target"
        )
        init.add_argument(
            "project", default=None, type=str, help="name of your project"
        )

    @staticmethod
    def execute(args):
        conf = load_conf()

        project = args.project
        projects_folder = conf.get("project_path")
        project_folder = os.path.join(projects_folder, project)

        source_folder = os.path.join(project_folder, "Source")
        server_target = os.path.join(source_folder, f"{project}Server.Target.cs")

        if os.path.exists(server_target):
            print(f"{server_target} already exists")
            return

        Dedicated.generate_server_target(project, server_target)

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


COMMAND = Dedicated
