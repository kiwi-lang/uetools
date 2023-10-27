import json
import os
from dataclasses import dataclass
from typing import Optional

from argklass.command import Command

from uetools.core.conf import find_project
from uetools.core.options import projectfield
from uetools.core.run import run


class Install(Command):
    """Install a plugin to an unreal project.

    Examples
    --------

    .. code-block::

        # This will install the plugin inside RTSGame/Plugins/
        # it will download the repository on put it inside the RTSGame/Plugins/ folder
        uecli install --project RTSGame VoxelPlugin https://github.com/Phyronnaz/VoxelPlugin --enable

        # This will install the plugin inside RTSGame/Plugins/
        # it will execute the following command:
        #   - git submodule add https://github.com/Phyronnaz/VoxelPlugin Plugins/VoxelPlugin
        #
        uecli install --project RTSGame VoxelPlugin https://github.com/Phyronnaz/VoxelPlugin --enable --destination Plugins --submodule

        # disable the plugin
        uecli disable --project RTSGame VoxelPlugin
    """

    name: str = "install"

    @dataclass
    class Arguments:
        # fmt: off

        plugin      : str                               # Plugin's name"
        url         : str                               # url of the plugin to install.
        project     : str           = projectfield()  # Name of the project to modify.
        destination : Optional[str] = 'Plugins'         # installation directory (defaults to: ``$PROJECT_NAME/Plugins/``)
        submodule   : bool          = False             # install the plugin as a git submodule (defaults to: ``False``)# fmt: on
        enable      : bool          = False             # Enable the plugin in the project settings
        force       : bool          = False             # submodule force
        # fmt: on

    @staticmethod
    def execute(args):
        project = find_project(args.project)
        folder = os.path.dirname(project)

        dest_relative = f"{args.destination}/{args.plugin}"
        dest = f"{folder}/{dest_relative}"

        errors = 0

        if not os.path.exists(dest):
            if args.submodule:
                force = ["--force"] if args.force else []
                cmd = ["git", "submodule", "add"] + force + ["--depth", "1", args.url, dest_relative]
            else:
                cmd = ["git", "clone", "--depth", "1", args.url, dest_relative]

            print(" ".join(cmd))
            errors += run(cmd, check=True, cwd=folder).returncode

        else:
            print(f"Folder {dest} exists already, skipping installation")

        if args.enable:
            project = find_project(args.project)

            with open(project, encoding="utf-8") as project_file:
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
