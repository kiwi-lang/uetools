from dataclasses import dataclass

from argklass.command import Command

from uetools.core.conf import find_project, uat
from uetools.core.run import popen_with_format
from uetools.core.util import command_builder
from uetools.format.cooking import CookingFormatter

from .arguments import BuildCookRunArguments

# ogMonitoredProcess: Running Serialized UAT: [ cmd.exe /c
# ""E:/UnrealEngine/Engine/Build/BatchFiles/RunUAT.bat"
#   -ScriptsForProject="E:/Examples/Acaraceim/Acaraceim.uproject"
#   Turnkey
#   -command=VerifySdk
#   -platform=Win64
#   -UpdateIfNeeded
#   -EditorIO
#   -EditorIOPort=54995
#   -project="E:/Examples/Acaraceim/Acaraceim.uproject"



@dataclass
class _CommonArgs(BuildCookRunArguments):
    nop4: bool = True
    utf8output : bool = True
    nocompileeditor: bool = True 
    skipbuildeditor: bool = True 
    cook: bool = True 
    stage: bool = True 
    package: bool = True 
    build: bool = True 
    pak: bool = True 
    iostore : bool = True
    compressed : bool = True
    prereqs : bool = True
    manifests : bool = True
    nocompile: bool = True
    nocompileuat: bool = True


@dataclass
class DedicatedServerCookArgs(_CommonArgs):
    server : bool = True
    noclient : bool = True


@dataclass
class ClientCookArgs(_CommonArgs):
    client : bool = True


@dataclass
class GameCookArgs(_CommonArgs):
    pass


profiles = {
    'server': DedicatedServerCookArgs,
    "game": GameCookArgs,
    "client": ClientCookArgs,
}


class CookGameUAT(Command):
    """Cook your main game using UAT"""

    name: str = "cook"

    # fmt: off
    @dataclass
    class Arguments(BuildCookRunArguments):
        build                                  : bool = True

        profile                                : str = None
        cook                                   : bool = True
        stage                                  : bool = True
        package                                : bool = True 
        prereqs                                : bool = True
        distribution                           : bool = True
        pak                                    : bool = True
        iostore                                : bool = True
        compressed                             : bool = True

        unattended                             : bool = True
        utf8output                             : bool = True
        nop4                                   : bool = True
        nullrhi                                : bool = True
        nocompileeditor                        : bool = False
        nocompileuat                           : bool = True
        skipbuildeditor                        : bool = False
        nodebuginfo                            : bool = True
    # fmt: on

    @staticmethod
    def execute(args: BuildCookRunArguments):
        assert args.project is not None
        args = BuildCookRunArguments(**vars(args))

        args.project = find_project(args.project)

        if args.profile is not None:
            profile = profiles.get(args.profile, None)

            if profile is not None:
                from dataclasses import asdict
                vars(args).update(asdict(profile))

        if args.archivedirectory is not None:
            args.archive = True

        if args.config is not None:
            config = vars(args).pop("config")

            if args.is_server():
                args.serverconfig = config
                
            if args.is_client():
                args.clientconfig = config

        uat_args = command_builder(args)
        cmd = [uat()] + ["BuildCookRun"] + uat_args + ["-nocompileuat"]

        print(" ".join(cmd))

        fmt = CookingFormatter(24)
        fmt.print_non_matching = True

        returncode = popen_with_format(fmt, cmd, shell=False)
        fmt.summary()

        return returncode


COMMANDS = CookGameUAT
