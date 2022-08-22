import os
import json
import configparser

from gamekit.conf import load_conf, Command


class VSCode(Command):
    name: str = 'vscode'

    @staticmethod
    def arguments(subparsers):
        python = subparsers.add_parser(VSCode.name, help='change vscode settings to fetch unreal python stub')
        python.add_argument("name", type=str, help="Project name")

    @staticmethod
    def execute(args):
        VSCode.enable_python_editor(args)
        VSCode.add_stub_to_path(args)

    @staticmethod
    def enable_python_editor(args):
        projects_folder = load_conf().get('project_path')
        project_folder = os.path.join(projects_folder, args.name)

        conf = os.path.join(project_folder, 'Config')
        default_engine = os.path.join(conf, 'DefaultEngine.ini')

        config = configparser.ConfigParser()
        config.read(default_engine)

        python_section = "/Script/PythonScriptPlugin.PythonScriptPluginUserSettings"
        config[python_section]["bDeveloperMode"] = 'True'
        config[python_section]["bEnableContentBrowserIntegration"] = 'True'

        with open(default_engine, 'w') as file:
            config.write(file)

    @staticmethod
    def add_stub_to_path(args):
        name = args.name
        projects_folder = load_conf().get('project_path')

        project_folder = os.path.join(projects_folder, name)
        vscode_folder = os.path.join(project_folder, '.vscode')
        vscode_settings = os.path.join(vscode_folder, 'settings.json')

        if not os.path.exists(vscode_settings):
            create_file = None

            while create_file not in ('Y', 'N'):
                create_file = input(f".vscode/settings.json does not exist, create ? (Y/N):")
                create_file = create_file.upper()

            if create_file == 'Y':
                os.makedirs(vscode_folder, exist_ok=True)
                with open(vscode_settings, 'w') as file:
                    file.write('{}')
            else:
                print('Nothing to do')
                return

        with open(vscode_settings, 'r') as file:
            vssetting = json.load(file)

        autocomplete_key = "python.autocomplete.extraPaths"
        analysis_key = "python.analysis.extraPaths"

        extra_paths = vssetting.get(autocomplete_key, [])
        extra_paths.append(os.path.join(project_folder, 'Intermediate', 'PythonStub'))
        extra_paths = list(set(extra_paths))
        vssetting[autocomplete_key] = extra_paths

        extra_paths = vssetting.get(analysis_key, [])
        extra_paths.append(os.path.join(project_folder, 'Intermediate', 'PythonStub'))
        extra_paths = list(set(extra_paths))
        vssetting[analysis_key] = extra_paths

        with open(vscode_settings, 'w') as file:
            json.dump(vssetting, file, indent=2)


COMMAND = VSCode
