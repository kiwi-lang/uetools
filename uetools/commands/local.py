import os
import subprocess

from uetools.conf import Command, load_conf, uat


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
