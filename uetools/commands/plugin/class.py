import os
from dataclasses import dataclass

from uetools.args.command import Command
from uetools.core.conf import find_project
from uetools.core.util import deduce_project, deduce_plugin, deduce_module


def make_file_for_module(module_path, klass):
    for folder, ext in [("Private", ".cpp"), ("Public", ".h")]:
        base = os.path.join(module_path, folder)
        os.makedirs(base, exist_ok=True)

        filepath = os.path.join(base, klass[1:] + ext)

        with open(filepath, "w"):
            print(filepath)


class Class(Command):
    """Add a new class

    Examples
    --------

    .. code-block:: console

       # Create a new file
       uecli plugin class --project RTSGame --plugin RTSGamePlugin AMyClass
       uecli plugin class --project RTSGame --plugin RTSGamePlugin FMyStruct

       # The command is able to deduce the project and plugin if the current working directory is inside the project
       cd MyProject/Plugins/MyPlugins
       uecli plugin class FMyStruct

    """

    name: str = "class"

    @dataclass
    class Arguments:
        klass: str  # Class' name
        project: str = deduce_project()  # project's name
        plugin: str = deduce_plugin()  # Plugin's name"

    @staticmethod
    def execute(args):
        assert args.klass[0] in ("F", "U", "A", "T")

        module_root = deduce_module(os.getcwd())
        if module_root is not None:
            make_file_for_module(module_root, args.klass)
            return

        else:
            uproject = find_project(args.project)
            project_path = os.path.dirname(uproject)

            plugin_src = os.path.join(project_path, "Plugins", args.plugin, "Source")

            make_file_for_module(plugin_src, args.klass)
        return 0


COMMANDS = Class
