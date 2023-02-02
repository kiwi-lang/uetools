import os
import re
from dataclasses import dataclass
from typing import Optional

from uetools.core.command import Command, newparser
from uetools.core.conf import CONFIG, CONFIGNAME, get_version_tag, load_conf, save_conf


@dataclass
class Arguments:
    """Initialize the configuration file with unreal engine folders

    Attributes
    ----------
    engine: str
        Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)

    project: str
        Path to the unreal project folder (C:/Projects)

    version: str
        Engine version

    Examples
    --------

    .. code-block:: console

       uecli init --engine C:/opt/UnrealEngine/Engine --projects C:/opt/Projects

    """

    # fmt: off
    engine  : Optional[str] = None  # Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)
    projects: Optional[str] = None  # Path to the unreal project folder (C:/Projects)
    version : Optional[str] = None  # Unreal Engine Version (5.1)
    # fmt: on


BUILTIN_PATTERN = re.compile(r"UE_(?P<version>(([0-9]*)\.[0-9]*))")


def get_engine_version(path):
    # Prebuild installs have a path that contains UEM.MIN/
    result = BUILTIN_PATTERN.search(path)
    if result:
        version = result.groupdict().get("version")
        if version:
            return version

    return get_version_tag(path, "archive")


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

        EngineAdd.addengine(conf, args.version, engine_path)

        save_conf(conf)
        print(f"Updated Engine paths inside `{config}`")
        return 0


@dataclass
class EngineAddArguments:
    """Add an engine version

    Attributes
    ----------
    version: str
        Version of name of the engine version

    engine: str
        Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)

    Examples
    --------

    .. code-block:: console

       uecli engine-add --version src --engine C:/opt/UnrealEngine/Engine

    """

    # fmt: off
    version: Optional[str] = None   # Unreal Engine Version (5.1)
    engine : Optional[str] = None   # Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)
    force  : bool          = False  # Allow version override
    # fmt: on


class EngineAdd(Command):
    """Add an unreal engine version"""

    name: str = "engine-add"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, EngineAdd)
        parser.add_arguments(EngineAddArguments, dest="args")

    @staticmethod
    def execute(args):
        config = os.path.join(CONFIG, CONFIGNAME)
        conf = {}

        if os.path.exists(config):
            conf = load_conf()

        EngineAdd.addengine(conf, args.args.version, args.args.engine, args.args.force)

        save_conf(conf)
        return 0

    @staticmethod
    def addengine(conf, version, path, force=False):
        if version is None:
            version = get_engine_version(path)

        engines = conf.get("engines", dict())

        if version not in engines or force:
            engines[version] = path
        else:
            print(
                f"{version} already exists `{engines[version]}` use --force to override"
            )

        conf["engines"] = engines


COMMANDS = [Init, EngineAdd]
