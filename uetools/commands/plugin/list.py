import os

from uetools.args.command import Command, newparser
from uetools.core.conf import engine_folder, find_project


class List(Command):
    """List installed plugin"""

    name: str = "list"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, List)
        parser.add_argument("project", nargs="?", type=str, help="Project name")

    @staticmethod
    def execute(args):
        plugin_folder = os.path.join(engine_folder(), "Plugins", "Marketplace")

        if args.project:
            project = find_project(args.project)
            plugin_folder = os.path.join(os.path.dirname(project), "Plugins")

        if not os.path.exists(plugin_folder):
            print(f"No Plugins found inside {plugin_folder}")
            return

        print("Plugins:")
        for p in os.listdir(plugin_folder):
            print("   -", p)


COMMANDS = List
