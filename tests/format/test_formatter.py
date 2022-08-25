from uetools.format.base import Formatter
from uetools.format.cooking import CookingFormatter
from uetools.format.tests import TestFormatter

log_lines = """
LogWindows: Failed to load 'aqProf.dll' (GetLastError=126)
LogWindows: File 'aqProf.dll' does not exist
LogProfilingDebugging: Loading WinPixEventRuntime.dll for PIX profiling (from ../../../Engine/Binaries/ThirdParty/Windows/WinPixEventRuntime/x64).
LogConfig: Display: Loading HoloLens ini files took 0.02 seconds
LogConfig: Display: Loading Android ini files took 0.02 seconds
LogConfig: Display: Loading Unix ini files took 0.03 seconds
LogConfig: Display: Loading Windows ini files took 0.03 seconds
LogConfig: Display: Loading TVOS ini files took 0.03 seconds
LogConfig: Display: Loading Linux ini files took 0.03 seconds
LogConfig: Display: Loading LinuxArm64 ini files took 0.03 seconds
LogPluginManager: Mounting Engine plugin FastBuildController
"""

formatted = """
[  0][L][LogWindows              ] Failed to load 'aqProf.dll' (GetLastError=126)
[  0][L][LogWindows              ] File 'aqProf.dll' does not exist
[  0][L][LogProfilingDebugging   ] Loading WinPixEventRuntime.dll for PIX profiling (from ../../../Engine/Binaries/ThirdParty/Windows/WinPixEventRuntime/x64).
[  0][D][LogConfig               ]  Loading HoloLens ini files took 0.02 seconds
[  0][D][LogConfig               ]  Loading Android ini files took 0.02 seconds
[  0][D][LogConfig               ]  Loading Unix ini files took 0.03 seconds
[  0][D][LogConfig               ]  Loading Windows ini files took 0.03 seconds
[  0][D][LogConfig               ]  Loading TVOS ini files took 0.03 seconds
[  0][D][LogConfig               ]  Loading Linux ini files took 0.03 seconds
[  0][D][LogConfig               ]  Loading LinuxArm64 ini files took 0.03 seconds
[  0][L][LogPluginManager        ] Mounting Engine plugin FastBuildController
"""

cooking_lines = """
LogCookCommandlet: Display: DDC Resource Stats
LogCookCommandlet: Display: =======================================================================================================
LogCookCommandlet: Display: Asset Type                          Total Time (Sec)  GameThread Time (Sec)  Assets Built  MB Processed
LogCookCommandlet: Display: ----------------------------------  ----------------  ---------------------  ------------  ------------
LogCookCommandlet: Display: Texture (Streaming)                             0.31                   0.00             0        148.17
LogCookCommandlet: Display: SkeletalMesh                                    0.30                   0.00             0         83.64
LogCookCommandlet: Display: MaterialShader                                  0.21                   0.21             0          6.95
LogCookCommandlet: Display: PhysX (BodySetup)                               0.02                   0.01             0          4.06
LogCookCommandlet: Display: DistanceField                                   0.02                   0.00             0          3.36
LogCookCommandlet: Display: StaticMesh                                      0.02                   0.00             0          3.42
LogCookCommandlet: Display: AnimSequence                                    0.01                   0.01             0          3.30
LogCookCommandlet: Display: GlobalShader                                    0.01                   0.01             0         12.43
LogCookCommandlet: Display: NavCollision                                    0.01                   0.00             0          0.06
LogCookCommandlet: Display: CardRepresentation                              0.01                   0.00             0          0.03
LogCookCommandlet: Display: NiagaraScript                                   0.01                   0.01             0          0.00
LogCookCommandlet: Display: Texture (Inline)                                0.00                   0.00             0         46.51
LogPackageBuildDependencyTracker: Display: Package Accesses (330 referencing packages with a total of 2087 unique accesses)
LogCore: Engine exit requested (reason: Commandlet CookCommandlet_0 finished execution (result 0))
LogInit: Display:
LogInit: Display: Success - 0 error(s), 0 warning(s)
LogInit: Display:
Execution of commandlet took:  4.14 seconds
LogCore: Engine exit requested (reason: EngineExit() was called; note: exit was already requested)
LogStaticMesh: Abandoning remaining async distance field tasks for shutdown
LogStaticMesh: Abandoning remaining async card representation tasks for shutdown
LogExit: Preparing to exit.
LogUObjectHash: Compacting FUObjectHashTables data took   1.10ms
LogWorld: UWorld::CleanupWorld for Untitled, bSessionEnded=true, bCleanupResources=true
LogDemo: Cleaned up 0 splitscreen connections with owner deletion
LogStylusInput: Shutting down StylusInput subsystem.
LogLevelSequenceEditor: LevelSequenceEditor subsystem deinitialized.
LogExit: Editor shut down
LogExit: Object subsystem successfully closed.
"""

formatted_cooking = (
    """
[D][LogCookCommandlet       ]  DDC Resource Stats
[D][LogCookCommandlet       ]  =======================================================================================================
[D][LogCookCommandlet       ]  Asset Type                          Total Time (Sec)  GameThread Time (Sec)  Assets Built  MB Processed
[D][LogCookCommandlet       ]  ----------------------------------  ----------------  ---------------------  ------------  ------------
[D][LogCookCommandlet       ]  Texture (Streaming)                             0.31                   0.00             0        148.17
[D][LogCookCommandlet       ]  SkeletalMesh                                    0.30                   0.00             0         83.64
[D][LogCookCommandlet       ]  MaterialShader                                  0.21                   0.21             0          6.95
[D][LogCookCommandlet       ]  PhysX (BodySetup)                               0.02                   0.01             0          4.06
[D][LogCookCommandlet       ]  DistanceField                                   0.02                   0.00             0          3.36
[D][LogCookCommandlet       ]  StaticMesh                                      0.02                   0.00             0          3.42
[D][LogCookCommandlet       ]  AnimSequence                                    0.01                   0.01             0          3.30
[D][LogCookCommandlet       ]  GlobalShader                                    0.01                   0.01             0         12.43
[D][LogCookCommandlet       ]  NavCollision                                    0.01                   0.00             0          0.06
[D][LogCookCommandlet       ]  CardRepresentation                              0.01                   0.00             0          0.03
[D][LogCookCommandlet       ]  NiagaraScript                                   0.01                   0.01             0          0.00
[D][LogCookCommandlet       ]  Texture (Inline)                                0.00                   0.00             0         46.51
[D][LogPackageBuildDependencyTracker]  Package Accesses (330 referencing packages with a total of 2087 unique accesses)
[L][LogCore                 ] Engine exit requested (reason: Commandlet CookCommandlet_0 finished execution (result 0))
[D][LogInit                 ] """
    + """
[D][LogInit                 ]  Success - 0 error(s), 0 warning(s)
[D][LogInit                 ] """
    + """
Execution of commandlet took:  4.14 seconds[L][LogCore                 ] Engine exit requested (reason: EngineExit() was called; note: exit was already requested)
[L][LogStaticMesh           ] Abandoning remaining async distance field tasks for shutdown
[L][LogStaticMesh           ] Abandoning remaining async card representation tasks for shutdown
[L][LogExit                 ] Preparing to exit.
[L][LogUObjectHash          ] Compacting FUObjectHashTables data took   1.10ms
[L][LogWorld                ] UWorld: :CleanupWorld for Untitled, bSessionEnded=true, bCleanupResources=true
[L][LogDemo                 ] Cleaned up 0 splitscreen connections with owner deletion
[L][LogStylusInput          ] Shutting down StylusInput subsystem.
[L][LogLevelSequenceEditor  ] LevelSequenceEditor subsystem deinitialized.
[L][LogExit                 ] Editor shut down
[L][LogExit                 ] Object subsystem successfully closed.
"""
)

testing_lines = """
"""

formatted_testing = """

"""


def test_formatter(capsys):
    fmt = Formatter(24)

    for line in log_lines.split("\n"):
        fmt.match_regex(line)

    captured = capsys.readouterr()

    assert captured.out.strip() == formatted.strip()


def test_formatter_cook(capsys):
    fmt = CookingFormatter(24)

    for line in cooking_lines.split("\n"):
        fmt.match_regex(line)

    captured = capsys.readouterr()

    print()
    print(captured.out.strip())
    print()

    assert captured.out.strip() == formatted_cooking.strip()


def test_formatter_test(capsys):
    fmt = TestFormatter(24)

    for line in log_lines.split("\n"):
        fmt.match_regex(line)

    captured = capsys.readouterr()
    assert captured.out.strip() == formatted.strip()
