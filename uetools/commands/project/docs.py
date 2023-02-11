import os
from typing import Optional

from cookiecutter.main import cookiecutter

from uetools.core.command import Command, newparser
from uetools.core.conf import find_project

COOKIECUTTER = "https://github.com/kiwi-lang/UEDocs"


# pylint: disable=too-few-public-methods
class Arguments:
    # fmt: off
    project : str                    # name of your project
    no_input: bool          = False  # Do not show user prompts
    config  : Optional[str] = None   # Configuration file used to initialize the project (json)
    # fmt: on


class Docs(Command):
    """Add a Sphinx + Doxygen documentation to a project

    Attributes
    ----------
    name: str
        Name of the project

    """

    name: str = "docs"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Docs)
        parser.add_argument("project", type=str, help="")
        parser.add_argument(
            "--no-input",
            action="store_true",
            default=False,
            help="",
        )
        parser.add_argument(
            "--config",
            type=str,
            default=None,
            help="",
        )

    @staticmethod
    def execute(args):
        uproject = find_project(args.project)
        folder = os.path.dirname(uproject)

        os.chdir(folder)
        cookiecutter(
            COOKIECUTTER,
            no_input=args.no_input,
            config_file=args.config,
            overwrite_if_exists=True,
        )

        return 0


COMMANDS = Docs
