import os
from dataclasses import dataclass
from typing import Optional

from uetools.core.command import Command, newparser
from uetools.core.conf import CONFIG, CONFIGNAME, load_conf, save_conf


@dataclass
class Arguments:
    """Initialize the configuration file with unreal engine folders

    Attributes
    ----------
    engine: str
        Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)

    project: str
        Path to the unreal project folder (C:/Projects)

    Examples
    --------

    .. code-block:: console

       uecli init --engine C:/opt/UnrealEngine/Engine --projects C:/opt/Projects

    """

    engine: Optional[
        str
    ] = None  # Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)
    projects: Optional[str] = None  # Path to the unreal project folder (C:/Projects)


class Init(Command):
    """Initialize the configuration file for the command line interface"""

    name: str = "init"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, Init)
        parser.add_arguments(Arguments, dest="init")

    @staticmethod
    def execute(args):
        """Initialize the engine and projects folders"""
        args = args.init

        config = os.path.join(CONFIG, CONFIGNAME)
        conf = {}

        default_engine = "/UnrealEngine/Engine"
        default_project = os.path.abspath(os.path.join("..", default_engine))

        if os.path.exists(config):
            conf = load_conf()
            default_engine = conf.get("engine_path", default_engine)
            default_project = conf.get("project_path", default_project)

        if args.engine is None:
            engine_path = input(f"Engine Folder [{default_engine}]: ")
        else:
            engine_path = args.engine

        if args.projects is None:
            project_folders = input(f"Project Folder [{default_project}]: ")
        else:
            project_folders = args.projects

        engine_path = engine_path or default_engine
        project_folders = project_folders or default_project

        conf["engine_path"] = engine_path
        conf["project_path"] = project_folders

        save_conf(conf)
        print(f"Updated Engine paths inside `{config}`")
        return 0


COMMANDS = Init
