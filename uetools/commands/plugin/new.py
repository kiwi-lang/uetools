import json
import os
import tempfile

import pkg_resources

from uetools.args.command import Command, newparser
from uetools.core.conf import find_project


class NewPlugin(Command):
    """Create a new plugin from a template"""

    name: str = "new"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, NewPlugin)
        parser.add_argument(
            "project", type=str, help="Project in which the plugin will live"
        )
        parser.add_argument("plugin", type=str, help="Name of the plugin")

    @staticmethod
    def execute(args):
        from cookiecutter.main import cookiecutter

        project = find_project(args.project)
        project_dir = os.path.dirname(project)

        template = pkg_resources.resource_filename(
            __name__, "templates/PluginTemplate/cookiecutter.json"
        )

        assert os.path.exists(template)
        template = os.path.dirname(template)
        assert os.path.exists(template)

        configfile = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump({"default_context": {"plugin_name": args.plugin}}, configfile)
        configfile.flush()

        plugin_dir = os.path.join(project_dir, "Plugins")
        assert os.path.exists(plugin_dir)

        kwargs = dict(
            no_input=True,
            config_file=configfile.name,
            overwrite_if_exists=True,
            output_dir=plugin_dir,
        )

        cookiecutter(
            template,
            **kwargs,
        )

        # Windows have permission issues on reading a temporary files
        configfile.close()
        os.remove(configfile.name)


COMMANDS = NewPlugin
