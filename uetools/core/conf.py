"""Defines constants and utility used throughout the project"""
import json
import os
import platform

from appdirs import user_config_dir

NAME = "uecli"
AUTHOR = "uetools"
CONFIG = user_config_dir(NAME, AUTHOR)
CONFIGNAME = "loc.json"
LATEST_CONF = None
WINDOWS = platform.system().startswith("Windows")
OSX = platform.system().startswith("Darwin")
LINUX = not WINDOWS and not OSX


def get_build_modes():
    """Returns the build modes supported by UBT"""
    return ["Tests", "Debug", "Development", "Shipping"]


def build_platform_from_editor(editor_platform):
    """Maps editor target to build target"""
    if editor_platform.startswith("Windows"):
        return "Win64"

    return "Linux"


def guess_platform():
    """Try to guess the platform we are building for"""
    if WINDOWS:
        return "Win64"

    if OSX:
        return "Mac"

    return "Linux"


def guess_editor_platform():
    """Try to guess for which platform we are trying to build for"""
    if WINDOWS:
        return "Windows"

    # this is probably wrong
    if OSX:
        return "Mac"

    return "Linux"


def load_conf():
    """Loads the configuration from the config file"""
    # pylint: disable=global-statement
    global LATEST_CONF

    config = os.path.join(CONFIG, CONFIGNAME)
    os.makedirs(CONFIG, exist_ok=True)

    if not os.path.exists(config):
        return {}

    with open(config, "r", encoding="utf-8") as conffile:
        conf = json.load(conffile)

    LATEST_CONF = conf
    return conf


def save_conf(conf):
    """Saves the given configuration to the config file"""
    config = os.path.join(CONFIG, CONFIGNAME)
    os.makedirs(CONFIG, exist_ok=True)

    with open(config, "w", encoding="utf-8") as conffile:
        json.dump(conf, conffile)


def update_conf(**kwargs):
    """Updates the configuration with the given key-value pairs"""
    conf = load_conf()
    conf.update(kwargs)
    save_conf(conf)


def binary(name):
    """Returns the name of a binary for the current platform"""
    if WINDOWS:
        return name + ".exe"

    return name


def bash(name):
    """Returns the name of a script for the current platform"""
    if WINDOWS:
        return name + ".bat"

    # if OSX:
    #    return name + '.command'

    return name + ".sh"


def ubt():
    """Returns the path to the unreal build tools executable"""
    engine = engine_folder()

    if WINDOWS:
        return os.path.join(
            engine, "Binaries", "DotNET", "UnrealBuildTool", binary("UnrealBuildTool")
        )

    return os.path.join(engine, "Build", "BatchFiles", "Linux", "Build.sh")


def uat():
    """Returns the path to the unreal automation executable"""
    engine = engine_folder()

    if WINDOWS:
        return os.path.join(engine, "Build", "BatchFiles", bash("RunUAT"))

    return os.path.join(engine, "Build", "BatchFiles", bash("RunUAT"))


def editor():
    """Returns the path to the editor executable"""
    engine = engine_folder()

    if WINDOWS:
        return os.path.join(
            engine,
            "Binaries",
            "Win64",
            binary("UnrealEditor"),
        )

    return os.path.join(
        engine,
        "Binaries",
        "Linux",
        binary("UnrealEditor"),
    )


def editor_cmd():
    """Returns the path to the editor executable (cmd version)"""
    engine = engine_folder()

    if WINDOWS:
        return os.path.join(
            engine,
            "Binaries",
            "Win64",
            binary("UnrealEditor-Cmd"),
        )

    return os.path.join(
        engine,
        "Binaries",
        "Linux",
        binary("UnrealEditor-Cmd"),
    )


# Supported platforms are listed here
#       UnrealEngine\Engine\Source\Programs\UnrealBuildTool\Platform
#
UBT_PLATFORMS = {
    "Android",
    "HoloLens",
    "IOS",
    "Linux",
    "LinuxArm64",
    "Mac",
    "TVOS",
    "Win64",
}


def get_build_platforms():
    """Returns the platforms supported by UBT"""
    return UBT_PLATFORMS


EDITOR_PLATOFRMS = {
    "Android",
    "Android_ASTC",
    "Android_DXT",
    "Android_ETC2",
    "AndroidClient",
    "Android_ASTCClient",
    "Android_DXTClient",
    "Android_ETC2Client",
    "Android_Multi",
    "Android_MultiClient",
    "HoloLens",
    "HoloLensClient",
    "Windows",
    "WindowsEditor",
    "WindowsServer",
    "WindowsClient",
    "LinuxArm64",
    "LinuxArm64Server",
    "LinuxArm64Client",
    "Linux",
    "LinuxServer",
    "LinuxClient",
    "LinuxEditor",
}


def get_editor_platforms():
    """returns the platforms supported by the editor"""
    return EDITOR_PLATOFRMS


def find_project(name):
    """Returns the path to the project file

    Examples
    --------

    .. code-block:: python

       find_project('RTSGame')
       /op/project/RTSGame/RTSGame.uproject

       # if the game is inside the engine repository
       find_project('RTSGame')
       /op/UnrealEngine/RTSGame/RTSGame.uproject

       find_project('/op/project/RTSGame/RTSGame.uproject')
       /op/project/RTSGame/RTSGame.uproject

       # project name is extracted from target
       find_project('RTSGameEditor')
       /op/project/RTSGame/RTSGame.uproject

       find_project('RTSGameServer')
       /op/project/RTSGame/RTSGame.uproject

    """

    if os.path.isabs(name) and name.endswith(".uproject"):
        return name

    if name.endswith(".uproject"):
        name = name[:-9]

    if name.endswith("Editor"):
        name = name[:-6]

    elif name.endswith("Server"):
        name = name[:-6]

    elif name.endswith("Client"):
        name = name[:-6]

    folder = os.path.join(project_folder(), name)
    uproject_project = os.path.join(folder, f"{name}.uproject")

    if os.path.exists(uproject_project):
        return uproject_project

    uproject_engine = os.path.join(engine_root(), name, f"{name}.uproject")

    if os.path.exists(uproject_engine):
        return uproject_engine

    raise RuntimeError(f"None of {uproject_project}, {uproject_engine} exist")


def project_folder():
    """Returns the folder user to store projects"""
    return load_conf().get("project_path")


def engine_folder():
    """returns the engine folder ``UnrealEngine/Engine``"""
    return load_conf().get("engine_path")


def engine_root():
    """returns the engine root ``UnrealEngine``"""
    return os.path.abspath(os.path.join(engine_folder(), ".."))


def ready():
    """Returns true if uetools was initialized"""
    return load_conf().get("project_path") is not None
