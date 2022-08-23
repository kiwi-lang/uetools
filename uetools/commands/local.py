import os
import subprocess
from dataclasses import dataclass

from simple_parsing import choice

from uetools.command import Command
from uetools.conf import load_conf, uat

actions = ["Gather", "Compile", "import", "export"]


@dataclass
class Arguments:
    """Generate localization files"""

    name: str
    action: choice(*actions)


class Local(Command):
    """Generate localization files"""

    name: str = "local"

    @staticmethod
    def arguments(subparsers):
        init = subparsers.add_parser(Local.name, help="Initialize engine location")
        init.add_argument(
            "project", default=None, type=str, help="name of your project"
        )
        init.add_argument(
            "action", default=None, type=str, help="Gather, Compile, import, export"
        )

    @staticmethod
    def execute(args):
        name = args.project

        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, name)
        uproject = os.path.join(project_folder, f"{name}.uproject")

        args = [
            uat(),
            uproject,
            "-run=GatherText",
            "-config=Config/Localization/Game_Gather.ini",
            "-EnableSCC",
            "-DisableSCCSubmit",
        ]

        subprocess.run(
            args, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True
        )


COMMAND = Local
