

import os
from dataclasses import dataclass

from uetools.core.command import Command, newparser
from uetools.core.conf import find_project
from uetools.core.util import deduce_project_plugin, deduce_module


@dataclass
class Arguments:
    name: str
    plugin: str



def make_file_for_module(module_path, klass):
    for folder, ext in [('Private', '.cpp'), ("Public", '.h')]:

        base = os.path.join(module_path, folder)
        os.makedirs(base, exist_ok=True)

        filepath = os.path.join(base, klass[1:] + ext)   

        with open(filepath, 'w'):
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

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Class)

        project, plugin = deduce_project_plugin(os.getcwd())

        parser.add_argument("--project", type=str, help="project's name", default=project)
        parser.add_argument("--plugin", type=str, help="Plugin's name", default=plugin)
        parser.add_argument("klass", type=str, help="Class' name")

    @staticmethod
    def execute(args):
        assert args.klass[0] in ('F', 'U', 'A', 'T')

        module_root = deduce_module(os.getcwd())
        if module_root is not None:
            make_file_for_module(module_root, args.klass)
            return

        else:
            uproject = find_project(args.project)
            project_path = os.path.dirname(uproject)

            plugin_src = os.path.join(project_path, 'Plugins', args.plugin, 'Source')

            make_file_for_module(plugin_src, args.klass)
        return 0


COMMANDS = Class
