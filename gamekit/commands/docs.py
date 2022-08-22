import os
import pkg_resources

from gamekit.conf import load_conf, save_conf, CONFIG, CONFIGNAME, Command

from cookiecutter.main import cookiecutter


COOKIECUTTER = "https://github.com/Delaunay/UEDocs"


class Docs(Command):
    """Add a docs folder to your project"""

    # TODO: create a cookiecutter for Unreal projects documentation

    name: str = "docs"

    @staticmethod
    def arguments(subparsers):
        init = subparsers.add_parser(
            Docs.name, help="Add documentation to your project"
        )
        init.add_argument(
            "project", default=None, type=str, help="name of your project"
        )

    @staticmethod
    def execute(args):
        project = args.project

        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, project)

        os.chdir(project_folder)
        cookiecutter(COOKIECUTTER)


COMMAND = Docs
