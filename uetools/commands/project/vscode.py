import json
import os
from dataclasses import dataclass

from argklass.command import Command

from uetools.core.conf import find_project
from uetools.core.ini import UnrealINIParser
from uetools.core.options import projectfield


class VSCode(Command):
    """Tweak your VSCode setting for this project to find python stub generated by Unreal Engine.
    This will enable you to get autocomplete for Unreal Engine classes and functions.

    Notes
    -----

    It tweaks both your project settings and your vs code settings.

    """

    name: str = "vscode"

    @dataclass
    class Arguments:
        # fmt: off
        project      : str  = projectfield() # Project name
        yes          : bool = False            # No user prompts (assume yes)
        # fmt: on

    @staticmethod
    def execute(args):
        VSCode.enable_python_editor(args)
        VSCode.add_stub_to_path(args)
        return 0

    @staticmethod
    def enable_python_editor(args):
        """Modify your project settings to enable python scripting in your project"""
        project = find_project(args.project)
        folder = os.path.dirname(project)

        conf = os.path.join(folder, "Config")
        default_engine = os.path.join(conf, "DefaultEngine.ini")

        with open(default_engine, encoding="utf-8") as file:
            config = UnrealINIParser(file)

        python_section = "/Script/PythonScriptPlugin.PythonScriptPluginUserSettings"
        config.insert(python_section, "bDeveloperMode", "True")
        config.insert(python_section, "bEnableContentBrowserIntegration", "True")

        with open(default_engine, "w", encoding="utf-8") as file:
            config.write(file)

    @staticmethod
    def add_stub_to_path(args):
        """Modify vscode settings to add the python stub path to the autocomplete path."""
        name = args.project

        project = find_project(name)
        folder = os.path.dirname(project)

        vscode_folder = os.path.join(folder, ".vscode")
        vscode_settings = os.path.join(vscode_folder, "settings.json")

        if not os.path.exists(vscode_settings):
            create_file = "Y" if args.yes else None

            while create_file not in ("Y", "N"):
                create_file = input(".vscode/settings.json does not exist, create ? (Y/N):")
                create_file = create_file.upper()

            if create_file == "Y":
                os.makedirs(vscode_folder, exist_ok=True)
                with open(vscode_settings, "w", encoding="utf-8") as file:
                    file.write("{}")
            else:
                print("Nothing to do")
                return

        with open(vscode_settings, encoding="utf-8") as file:
            vssetting = json.load(file)

        autocomplete_key = "python.autocomplete.extraPaths"
        analysis_key = "python.analysis.extraPaths"

        extra_paths = vssetting.get(autocomplete_key, [])
        extra_paths.append(os.path.join(folder, "Intermediate", "PythonStub"))
        extra_paths = list(set(extra_paths))
        vssetting[autocomplete_key] = extra_paths

        extra_paths = vssetting.get(analysis_key, [])
        extra_paths.append(os.path.join(folder, "Intermediate", "PythonStub"))
        extra_paths = list(set(extra_paths))
        vssetting[analysis_key] = extra_paths

        with open(vscode_settings, "w", encoding="utf-8") as file:
            json.dump(vssetting, file, indent=2)


COMMANDS = VSCode
