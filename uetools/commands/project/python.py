import os
from dataclasses import dataclass
from io import UnsupportedOperation

from argklass.command import Command

from uetools.core.conf import editor, find_project
from uetools.core.ini import UnrealINIParser
from uetools.core.options import projectfield


class Python(Command):
    """Tweak your project settings to enable python scripting in your project

    Attributes
    ----------
    project: str
        Name of the project

    """

    name: str = "python"

    @dataclass
    class Arguments:
        project: str = projectfield()  # name of your project

    @staticmethod
    def execute(args):
        project = find_project(args.project)
        folder = os.path.dirname(project)

        conf = os.path.join(folder, "Config")
        default_engine = os.path.join(conf, "DefaultEngine.ini")

        with open(default_engine, encoding="utf-8") as file:
            config = UnrealINIParser(file)

        python_section = "/Script/PythonScriptPlugin.PythonScriptPluginUserSettings"
        config.insert(python_section, "bDeveloperMode", "True")
        config.insert(python_section, "bEnableContentBrowserIntegration", "True")

        python_setting = "/Script/PythonScriptPlugin.PythonScriptPluginSettings"
        config.insert(python_setting, "bDeveloperMode", "True")

        if os.path.exists(os.path.join(folder, args.project, "Plugings", "Gamekit")):
            base_path = os.path.join(args.project, "Plugins", "Gamekit", "Script")
            relative_path = os.path.relpath(folder, os.path.dirname(editor()))
            final_path = os.path.join(relative_path, base_path)
            config.insert(python_setting, "+AdditionalPaths", f'(Path="{final_path}")')

        try:
            with open(default_engine, "w", encoding="utf-8") as file:
                config.write(file)

            return 0
        except UnsupportedOperation:
            print("Could not save config")
            print("Is unreal engine open ?")
            raise


COMMANDS = Python
