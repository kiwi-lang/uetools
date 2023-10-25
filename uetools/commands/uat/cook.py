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
#   BuildCookRun
#   -nop4
#   -utf8output
#   -nocompileeditor
#   -skipbuildeditor
#   -cook
#   -project="E:/Examples/Acaraceim/Acaraceim.uproject"
#   -target=AcaraceimClient
#   -unrealexe="E:\UnrealEngine\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
#   -platform=Win64
#   -stage
#   -archive
#   -package
#   -build
#   -pak
#   -iostore
#   -compressed
#   -prereqs
#   -archivedirectory="E:/Examples/Acaraceim/Saved/StagedBuilds"
#   -client
#   -clientconfig=Shipping
#   -nodebuginfo"
#   -nocompile
#   -nocompileuat ]


class CookGameUAT(Command):
    """Cook your main game using UAT"""

    name: str = "cook"

    # fmt: off
    @dataclass
    class Arguments(BuildCookRunArguments):
        build                                  : bool = True

        cook                                   : bool = True
        stage                                  : bool = True

        prereqs                                : bool = True
        distribution                           : bool = True
        pak                                    : bool = True

        unattended                             : bool = True
        utf8output                             : bool = True
        noP4                                   : bool = True
        nullrhi                                : bool = True
        nocompileeditor                        : bool = True
        skipbuildeditor                        : bool = True
        nodebuginfo                            : bool = True
    # fmt: on

    @staticmethod
    def execute(args):
        assert args.project is not None

        args.project = find_project(args.project)

        uat_args = command_builder(args)
        cmd = [uat()] + ["BuildCookRun"] + uat_args + ["-nocompileuat"]

        print(" ".join(cmd))

        fmt = CookingFormatter(24)
        fmt.print_non_matching = True

        returncode = popen_with_format(fmt, cmd, shell=False)
        fmt.summary()

        return returncode


COMMANDS = CookGameUAT
