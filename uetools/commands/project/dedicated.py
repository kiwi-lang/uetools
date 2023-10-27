import os
from dataclasses import dataclass

from argklass.cache import load_resource
from argklass.command import Command

from uetools.core.conf import find_project
from uetools.core.options import projectfield


class Dedicated(Command):
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

    name: str = "dedicated"

    @dataclass
    class Arguments:
        project: str = projectfield()  # name of your project

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
        template = load_resource(__name__, "templates/TemplateServer.Target")

        with open(template, encoding="utf-8") as template_file:
            template = template_file.read()

        template = template.replace("{ProjectName}", project)

        with open(server_target, "w", encoding="utf-8") as file:
            file.write(template)


COMMANDS = Dedicated
