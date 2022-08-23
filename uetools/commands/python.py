import configparser
import os
from dataclasses import dataclass
from io import UnsupportedOperation

from uetools.command import Command
from uetools.conf import editor, load_conf


@dataclass
class Arguments:
    """Tweak your project settings to enable python scripting in your project"""

    project: str


class Python(Command):
    """Tweak your project settings to enable python scripting in your project"""

    name: str = "python"

    @staticmethod
    def arguments(subparsers):
        init = subparsers.add_parser(Python.name, help="Enable python for your project")
        init.add_argument(
            "project", default=None, type=str, help="name of your project"
        )

    @staticmethod
    def execute(args):
        projects_folder = load_conf().get("project_path")

        project_folder = os.path.join(projects_folder, args.project)

        conf = os.path.join(project_folder, "Config")
        default_engine = os.path.join(conf, "DefaultEngine.ini")

        config = configparser.ConfigParser(strict=False)
        config.read(default_engine)

        python_section = "/Script/PythonScriptPlugin.PythonScriptPluginUserSettings"
        config[python_section]["bDeveloperMode"] = "True"
        config[python_section]["bEnableContentBrowserIntegration"] = "True"

        base_path = os.path.join(args.project, "Plugins", "uetools", "Script")
        relative_path = os.path.relpath(projects_folder, os.path.dirname(editor()))
        final_path = os.path.join(relative_path, base_path)

        python_setting = "/Script/PythonScriptPlugin.PythonScriptPluginSettings"
        config[python_setting]["bDeveloperMode"] = "True"
        config[python_setting]["+AdditionalPaths"] = f'(Path="{final_path}")'

        try:
            with open(default_engine, "w", encoding="utf-8") as file:
                config.write(file)
        except UnsupportedOperation:
            print("Could not save config")
            print("Is unreal engine open ?")
            raise


COMMAND = Python
