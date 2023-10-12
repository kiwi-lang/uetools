import os
import re
from dataclasses import dataclass
from typing import Optional

from uetools.args.arguments import add_arguments
from uetools.args.command import Command, newparser
from uetools.core.conf import CONFIG, CONFIGNAME, get_version_tag, load_conf, save_conf

BUILTIN_PATTERN = re.compile(r"UE_(?P<version>(([0-9]*)\.[0-9]*))")


def get_engine_version(path):
    # Prebuild installs have a path that contains UEM.MIN/
    result = BUILTIN_PATTERN.search(path)
    if result:
        version = result.groupdict().get("version")
        if version:
            return version

    return get_version_tag(path, "archive")


@dataclass
class EngineAddArguments:
    # fmt: off
    version: Optional[str] = None  # Unreal Engine Version (5.1)
    engine: Optional[str] = None  # Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)
    force: bool = False  # Allow version override
    # fmt: on


class EngineAdd(Command):
    """Register an engine version

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

    name: str = "add"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, EngineAdd)
        add_arguments(parser, EngineAddArguments)

    @staticmethod
    def execute(args):
        config = os.path.join(CONFIG, CONFIGNAME)
        conf = {}

        if os.path.exists(config):
            conf = load_conf()

        EngineAdd.addengine(conf, args.version, args.engine, args.force)

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


COMMANDS = EngineAdd
