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

# LogTurnkeySupport: Completed SDK detection: ExitCode = 0
# LogMonitoredProcess: Running Serialized UAT: [ 
#   cmd.exe /c ""E:/UnrealEngine/Engine/Build/BatchFiles/RunUAT.bat"  
#       -ScriptsForProject="E:/Examples/Acaraceim/Acaraceim.uproject" Turnkey 
#       -utf8output -WaitForUATMutex -command=VerifySdk -ReportFilename="E:/Examples/Acaraceim/Intermediate/TurnkeyReport_1.log" 
#       -log="E:/Examples/Acaraceim/Intermediate/TurnkeyLog_1.log" -project="E:/Examples/Acaraceim/Acaraceim.uproject"  
#       -Device=Win64@KEPLER" 
#       -nocompile 
#       -nocompileuat 
# ]
# LogTurnkeySupport: Turnkey Platform: Android: (Status=Invalid, Allowed_Sdk=r25b, Current_Sdk=, Allowed_AutoSdk=r25b, Current_AutoSdk=, Flags="Platform_InvalidHostPrerequisites", Error="Android Studio is not installed correctly.")
# LogTurnkeySupport: Turnkey Platform: IOS: (Status=Invalid, MinAllowed_Sdk=1100.0.0.0, MaxAllowed_Sdk=8999.0, Current_Sdk=, Allowed_AutoSdk=14.1, Current_AutoSdk=, Flags="Platform_ValidHostPrerequisites")
# LogTurnkeySupport: Turnkey Platform: Linux: (Status=Invalid, Allowed_Sdk=v22_clang-16.0.6-centos7, Current_Sdk=, Allowed_AutoSdk=v22_clang-16.0.6-centos7, Current_AutoSdk=, Flags="Platform_ValidHostPrerequisites")
# LogTurnkeySupport: Turnkey Platform: LinuxArm64: (Status=Invalid, Allowed_Sdk=v22_clang-16.0.6-centos7, Current_Sdk=, Allowed_AutoSdk=v22_clang-16.0.6-centos7, Current_AutoSdk=, Flags="Platform_ValidHostPrerequisites")
# LogTurnkeySupport: Turnkey Platform: Mac: (Status=Invalid, MinAllowed_Sdk=1100.0.0.0, MaxAllowed_Sdk=8999.0, Current_Sdk=, Allowed_AutoSdk=14.1, Current_AutoSdk=, Flags="Platform_ValidHostPrerequisites")
# LogTurnkeySupport: Turnkey Platform: TVOS: (Status=Invalid, MinAllowed_Sdk=1100.0.0.0, MaxAllowed_Sdk=8999.0, Current_Sdk=, Allowed_AutoSdk=14.1, Current_AutoSdk=, Flags="Platform_ValidHostPrerequisites")
# LogTurnkeySupport: Turnkey Platform: Win64: (Status=Valid, MinAllowed_Sdk=10.0.00000.0, MaxAllowed_Sdk=10.9.99999.0, Current_Sdk=10.0.22621.0, Allowed_AutoSdk=10.0.18362.0, Current_AutoSdk=, Flags="InstalledSdk_ValidVersionExists")
# LogTurnkeySupport: Completed device detection: Code = 0
# LogMonitoredProcess: Running Serialized UAT: [ 
#   cmd.exe /c ""E:/UnrealEngine/Engine/Build/BatchFiles/RunUAT.bat"  
#   -ScriptsForProject="E:/Examples/Acaraceim/Acaraceim.uproject" Turnkey 
#   -command=VerifySdk -platform=Win64 -UpdateIfNeeded 
#   -EditorIO -EditorIOPort=54802  
#   -project="E:/Examples/Acaraceim/Acaraceim.uproject" 
#   BuildCookRun 
#   -nop4 -utf8output -nocompileeditor -skipbuildeditor -cook  
#   -project="E:/Examples/Acaraceim/Acaraceim.uproject" 
#   -target=Acaraceim 
#   -unrealexe="E:\UnrealEngine\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" -platform=Win64 
#   -stage -archive -package -build -pak -iostore -compressed 
#   -prereqs -archivedirectory="E:/tmp" -clientconfig=Development" -nocompile -nocompileuat ]
# LogTurnkeySupport: Turnkey Device: Win64@KEPLER: (Name=KEPLER, Type=Computer, Status=Valid, MinAllowed=10.0.18362.0, MaxAllowed=, Current=10.0.19045.0, Flags="Device_InstallSoftwareValid")


# BuildCookRun 
#   -project="D:\Builds\glrt--E4\0\moba383037\Acarac\Acaraceim.uproject" 
#   -build -cook -stage -package 
#   -archive -archivedirectory=D:\Builds\glrt--E4\0\moba383037\Acarac\Saved\Archives 
#   -platform=Win64 
#   -clientconfig=Development -target=Acaraceim -iostore -pak -pak -prereqs



@dataclass
class _CommonArgs(BuildCookRunArguments):
    nop4: bool = True
    utf8output : bool = True
    nocompileeditor: bool = True 
    skipbuildeditor: bool = True 
    build: bool = True
    cook: bool = True 
    stage: bool = True 
    package: bool = True 
    iostore : bool = True
    pak: bool = True 
    prereqs : bool = True
    compressed : bool = True
    manifests : bool = True
    nocompile: bool = True
    nocompileuat: bool = True
    archive: bool = True

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
        profile                                : str = None

        build                                  : bool = True
        cook                                   : bool = True
        package                                : bool = True
        stage                                  : bool = True
        prereqs                                : bool = True

        iostore                                : bool = True
        pak                                    : bool = True
        compressed                             : bool = True
        # unattended                            : bool = True
        # distribution                          : bool = True
        
        # Often set by the editor
        nop4                                   : bool = True
        utf8output                             : bool = True
        nocompileeditor                        : bool = False
        skipbuildeditor                        : bool = False
        nocompile                              : bool = False
        nocompileuat                           : bool = False
        nodebuginfo                            : bool = False
    # fmt: on

    @staticmethod
    def execute(args: BuildCookRunArguments):
        assert args.project is not None

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

            if BuildCookRunArguments.is_server(args):
                args.serverconfig = config
                
            if BuildCookRunArguments.is_client(args):
                args.clientconfig = config

        uat_args = [f"-ScriptsForProject=\"{args.project}\"", "Turnkey", "-UpdateIfNeeded", f"-project=\"{args.project}\""]
        build_cook_args = command_builder(args)

        cmd = [uat()] + uat_args + ["BuildCookRun"] + build_cook_args

        print(" ".join(cmd))

        fmt = CookingFormatter(24)
        fmt.print_non_matching = True

        returncode = popen_with_format(fmt, cmd, shell=False)
        fmt.summary()

        return returncode


COMMANDS = CookGameUAT
