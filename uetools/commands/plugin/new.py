from dataclasses import dataclass
import json
import os
import tempfile

from uetools.args.cache import load_resource
from uetools.args.command import Command
from uetools.core.conf import find_project
from uetools.core.util import deduce_project


class NewPlugin(Command):
    """Create a new plugin from a template"""

    name: str = "new"

    @dataclass
    class Arguments:
        plugin: str  # Plugin's name"
        project: str = deduce_project()  # project's name

    @staticmethod
    def execute(args):
        from cookiecutter.main import cookiecutter

        project = find_project(args.project)
        project_dir = os.path.dirname(project)

        template = load_resource(__name__, "templates/PluginTemplate/cookiecutter.json")

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
