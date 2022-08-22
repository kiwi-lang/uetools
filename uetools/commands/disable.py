import json
import os

from uetools.conf import Command, load_conf


class Disable(Command):
    """Disable unused plugin that are loading by default"""

    name: str = "disable"

    @staticmethod
    def arguments(subparsers):
        disable = subparsers.add_parser(
            Disable.name, help="Install uetools in a unreal project"
        )
        disable.add_argument("name", type=str, help="project's name")
        disable.add_argument("plugin", type=str, help="Plugin's name")

    @staticmethod
    def execute(args):
        name = args.name
        projects_folder = load_conf().get("project_path")
        project_folder = os.path.join(projects_folder, name)
        uproject = os.path.join(project_folder, f"{name}.uproject")

        with open(uproject, "r", encoding="utf-8") as project_file:
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


COMMAND = Disable
