import os

from cookiecutter.main import cookiecutter

from uetools.command import Command
from uetools.conf import load_conf

COOKIECUTTER = "https://github.com/kiwi-lang/UEDocs"


# pylint: disable=too-few-public-methods
class Arguments:
    """Add a Sphinx + Doxygen documentation to a project

    Attributes
    ----------
    name: str
        Name of the project

    """

    name: str


class Docs(Command):
    """Add a docs folder to your project"""

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
