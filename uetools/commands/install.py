import json
import os
from dataclasses import dataclass
from typing import Optional

from uetools.core.command import Command, newparser
from uetools.core.conf import find_project
from uetools.core.run import run


@dataclass
class Arguments:
    """Install a plugin to an unreal project.

    Attributes
    ----------
    name: str
        Name of the project to modify.

    url: str
        url of the plugin to install.

    destination:str
        installation directory (defaults to: ``$PROJECT_NAME/Plugins/``)

    submodule: bool
        install the plugin as a git submodule (defaults to: ``False``)

    Examples
    --------

    .. code-block::

        # This will install the plugin inside RTSGame/Plugins/
        #  it will download the repository on put it inside the RTSGame/Plugins/ folder
        uecli install RTSGame VoxelPlugin https://github.com/Phyronnaz/VoxelPlugin --enable

        # This will install the plugin inside RTSGame/Plugins/
        # it will execute the following command:
        #    - git submodule add https://github.com/Phyronnaz/VoxelPlugin Plugins/VoxelPlugin
        #
        uecli install RTSGame VoxelPlugin https://github.com/Phyronnaz/VoxelPlugin --enable --destination Plugins --submodule

        # disable the plugin
        uecli disable RTSGame VoxelPlugin
    """

    name: str
    url: str
    destination: Optional[str] = None
    submodule: bool = False


class Install(Command):
    """Install a plugin to an unreal project."""

    name: str = "install"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Install)
        parser.add_argument("name", type=str, help="Project name")
        parser.add_argument("plugin", type=str, help="name of the plugin")
        parser.add_argument("url", type=str, help="repository url of the plugin")
        parser.add_argument(
            "--enable",
            action="store_true",
            help="Enable the plugin in the project settings",
        )
        parser.add_argument(
            "--destination",
            type=str,
            default="Plugins",
            help="Plugin destination, relative to the root of the project",
        )
        parser.add_argument(
            "--submodule",
            action="store_true",
            default=False,
            help="add the plugin as a git submodule",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help="submodule force",
        )

    @staticmethod
    def execute(args):
        project = find_project(args.name)
        folder = os.path.dirname(project)

        dest_relative = f"{args.destination}/{args.plugin}"
        dest = f"{folder}/{dest_relative}"

        errors = 0

        if not os.path.exists(dest):
            if args.submodule:
                force = ["--force"] if args.force else []
                cmd = (
                    ["git", "submodule", "add"]
                    + force
                    + ["--depth", "1", args.url, dest_relative]
                )
            else:
                cmd = ["git", "clone", "--depth", "1", args.url, dest_relative]

            print(" ".join(cmd))
            errors += run(cmd, check=True, cwd=folder).returncode

        else:
            print(f"Folder {dest} exists already, skipping installation")

        if args.enable:
            project = find_project(args.name)

            with open(project, "r", encoding="utf-8") as project_file:
                project_conf = json.load(project_file)

            plugins = project_conf.get("Plugins", [])
            for plugin in plugins:

                if plugin.get("Name") == args.plugin:
                    plugin["Enabled"] = True
                    break

            else:
                # If Plugins array was missing, it was created above
                # insert it just in case
                project_conf["Plugins"] = plugins
                plugins.append(dict(Name=args.plugin, Enabled=True))

            with open(project, "w", encoding="utf-8") as project_file:
                json.dump(project_conf, project_file)

        return errors


COMMANDS = Install
