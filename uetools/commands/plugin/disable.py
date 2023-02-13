import json
from dataclasses import dataclass

from uetools.core.command import Command, newparser
from uetools.core.conf import find_project


@dataclass
class Arguments:
    name: str
    plugin: str


class Disable(Command):
    """Disable a plugin

    Examples
    --------

    .. code-block:: console

       # Disable the plugin
       uecli disable RTSGame RTSGamePlugin

    """

    name: str = "disable"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Disable)
        parser.add_argument("name", type=str, help="project's name")
        parser.add_argument("plugin", type=str, help="Plugin's name")

    @staticmethod
    def execute(args):
        name = args.name
        uproject = find_project(args.name)

        with open(uproject, encoding="utf-8") as project_file:
            project_conf = json.load(project_file)

        plugins = project_conf.get("Plugins")
        plugin_dict = {}

        for plugin in plugins:
            name = plugin["Name"]
            data = plugin

            plugin_dict[name] = data

        if args.plugin in plugin_dict:
            plugin_dict[args.plugin]["Enabled"] = False
        else:
            plugins.append(dict(Name=args.plugin, Enabled=False))

        with open(uproject, "w", encoding="utf-8") as project_file:
            json.dump(project_conf, project_file)

        return 0


COMMANDS = Disable
