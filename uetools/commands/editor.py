from __future__ import annotations

from dataclasses import dataclass

from uetools.core.command import Command, command_builder, newparser
from uetools.core.conf import editor_cmd, find_project
from uetools.core.run import popen_with_format
from uetools.format.base import Formatter

EDITOR_COMMANDSS = [
    # "debug {0}"
    "automation list",
    "runtests",
    "runall",
]

# fmt: off
@dataclass
class Vector:
    """Position vector"""
    x: float | None = 0
    y: float | None = 0
    z: float | None = 0

    def to_ue_cmd(self, name, cmd):
        """Convert the vector into a command line argument"""
        cmd.append(f"-{name}=(X={self.x},Y={self.y},Z={self.z})")


@dataclass
class Rotation:
    """Rotation vector"""
    pitch   : float | None = 0
    yaw     : float | None = 0
    roll    : float | None = 0

    def to_ue_cmd(self, name, cmd):
        """Convert the rotation into a command line argument"""
        cmd.append(f"-{name}=(Pitch={self.pitch},Yaw={self.yaw},Roll={self.roll})")


@dataclass
class DevArguments:
    """Development arguments"""
    abslog                   : str | None  = None  # Same as LOG= but without a filename length check.
    allusers                 : bool = False  # Add the game for all users when INSTALLGE is specified.
    auto                     : bool = False  # Assume yes on all questions. (for example during compile)
    autocheckoutpackages     : bool = False  # Automatically checkout packages that need to be saved.
    automatedmapbuild        : bool = False  # Perform an automated build of a specified map.
    biascompressionforsize   : bool = False  # Override compression settings with respect to size.
    buildmachine             : bool = False  # Set as build machine. Used for deciding if debug output is enabled.
    bulkimportingsounds      : bool = False  # Use when importing sounds in bulk. (Content Browser specific.)
    check_native_class_sizes : bool = False  # Enable checking of native class sizes. Note: Native classes on console platforms will cause native class size checks to fail even though they are assumed to be correct.
    codermode                : bool = False  # Enables Coder mode.
    compatscale              : bool = False  # Set compatibility settings manually to override PCCompat tool settings.
    conformdir               : bool = False  # Directory to use when conforming packages.
    cookfordemo              : bool = False  # Specify as cooking packages for the demo.
    cookpackages             : bool = False  # Tag to specify cooking packages.
    crashreports             : bool = False  # Always report crashes of the engine.
    d3ddebug                 : bool = False  # Use a d3d debug device.
    devcon                   : bool = False  # Disable secure connections for developers. (Uses unencrypted sockets.)
    dumpfileiostats          : bool = False  # Track and log File IO statistics.
    fixedseed                : bool = False  # Initialize the random number generator with a fixed value, 0.
    fixuptangents            : bool = False  # Fix legacy tangents in distributions automatically.
    forcelogflush            : bool = False  # Force a log flush after each line.
    forcepvrtc               : bool = False  # Force pvrtc texture compression for mobile platform.
    forcesoundrecook         : bool = False  # Force a complete re-cook of all sounds.
    genericbrowser           : bool = False  # Use the Generic Browser.
    installed                : bool = False  # For development purposes, run the game as if installed.
    installfw                : bool = False  # Set whether the handling of the firewall integration should be performed.
    uninstallfw              : bool = False  # Set whether the handling of the firewall integration should be performed.
    installge                : bool = False  # Add the game to the Game Explorer.
    cultureforcooking        : bool = False  # Set language to be used for cooking.
    lightmassdebug           : bool = False  # Launch lightmass manually with -debug and allow lightmass to be executed multiple times.
    lightmassstats           : bool = False  # Force all lightmass agents to report detailed stats to the log.
    log                      : str | None  = None  # When used as a switch (-log), opens a separate window to display the contents of the log in real time. When used as a setting (LOG=filename.log), tells the engine to use the log filename of the string that immediately follows.
    logtimes                 : bool = False  # Print time with log output. (Default, same as setting LogTimes=True in the [LogFiles] section of *Engine.ini.)
    noconform                : bool = False  # Tell the engine not to conform packages as they are compiled.
    nocontentbrowser         : bool = False  # Disable the Content Browser.
    noinnerexception         : bool = False  # Disable the exception handler within native C++.
    noloadstartuppackages    : bool = False  # Force startup packages not to be loaded. You can use this if objects in a startup package must be deleted from within the editor.
    nologtimes               : bool = False  # Do not print time with log output. (Same as setting LogTimes=False in the [LogFiles] section of *Engine.ini.)
    nopause                  : bool = False  # Close the log window automatically on exit.
    nopauseonsuccess         : bool = False  # Close the log window automatically on exit as long as no errors were present.
    norc                     : bool = False  # Disable the remote control. Used for dedicated servers.
    noverifygc               : bool = False  # Do not verify garbage compiler assumptions.
    nowrite                  : bool = False  # Disable output to log.
    seekfreeloading          : bool = False  # Only use cooked data.
    seekfreepackagemap       : bool = False  # Override the package map with the seekfree (cooked) version.
    seekfreeloadingpcconsole : bool = False  # Only use cooked data for PC console mode.
    seekfreeloadingserver    : bool = False  # Only use cooked data for server.
    setthreadnames           : bool = False  # (Xbox only) Force thread names to be set. This can mess up the XDK COM API which is why it must be explicitly set to be performed if desired.
    showmissingloc           : bool = False  # If missing localized text, return error string instead of English text.
    silent                   : bool = False  # Disable output and feedback.
    traceanimusage           : bool = False  # Trace animation usage.
    treatloadwarningsaserrors: bool = False  # Force load warnings to be treated as errors.
    unattended               : bool = False  # Set as unattended. Disable anything requiring feedback from user.
    uninstallge              : bool = False  # Remove the game from the Game Explorer.
    useunpublished           : bool = False  # Force packages in the Unpublished folder to be used.
    vadebug                  : bool = False  # Use the Visual Studio debugger interface.
    verbose                  : bool = False  # Set compiler to use verbose output.
    verifygc                 : bool = False  # Force garbage compiler assumptions to be verified.
    warningsaserrors         : bool = False  # Treat warnings as errors.


@dataclass
class RenderingArguments:
    """Rendering arguments"""
    consolex                : int | None   = None  # Set the horizontal position for console output window.
    consoley                : int | None   = None  # Set the vertical position for console output window.
    winx                    : int | None   = None  # Set the horizontal position of the game window on the screen.
    winy                    : int | None   = None  # Set the vertical position of the game window on the screen.
    resx                    : int | None   = None  # Set horizontal resolution for game window.
    resy                    : int | None   = None  # Set vertical resolution for game window.
    vsync                   : bool | None  = None  # Activate the VSYNC via command line. Pprevents tearing of the image but costs fps and causes input latency.)
    novsync                 : bool | None  = None  # Deactivate the VSYNC via command line.
    benchmark               : bool | None  = None  # Run game at fixed-step in order to process each frame without skipping any frames. This is useful in conjunction with DUMPMOVIE options.
    dumpmovie               : bool | None  = None  # Dump rendered frames to files using current resolution of game.
    exec                    : str | None   = None  # Executes the specified exec file.
    fps                     : int | None   = None  # Set the frames per second for benchmarking.
    fullscreen              : bool | None  = None  # Set game to run in fullscreen mode.
    seconds                 : float | None = None  # Set the maximum tick time.
    windowed                : bool | None  = None  # Set game to run in windowed mode.


@dataclass
class NetworkArguments:
    """Network arguments"""
    lanplay             : bool = False  # Tell the engine to not cap client bandwidth when connecting to servers. Causes double the amount of server updates and can saturate client's bandwidth.
    limitclientticks    : bool = False  # Force throttling of network updates.
    multihome           : bool = False  # Tell the engine to use a multihome address for networking.
    networkprofiler     : bool = False  # Enable network profiler tracking.
    nosteam             : bool = False  # Set steamworks to not be used.
    port                : int | None  = None  # Tell the engine to use a specific port number.
    primarynet          : bool = False  # Affect how the engine handles network binding.


@dataclass
class UserArguments:
    """User Arguments"""
    nohomedir           : bool = False  # Override use of My Documents folder as home directory.
    noforcefeedback     : bool = False  # Disable force feedback in the engine.
    nosound             : bool = False  # Disable any sound output from the engine.
    nosplash            : bool = False  # Disable use of splash image when loading the game.
    notexturestreaming  : bool = False  # Disable texture streaming. Highest quality textures are always loaded.
    onethread           : bool = False  # Run the engine using a single thread instead of multi-threading.
    paths               : str | None  = None  # Set what paths to use for testing wrangled content. Not used for shipping releases.
    preferredprocessor  : bool = False  # Set the thread affinity for a specific processor.
    useallavailablecores: bool = False  # Force the use of all available cores on the target platform.


@dataclass
class ServerArguments:
    """Server arguments"""
    login               : bool = False  # Set username to use when logging in.
    password            : bool = False  # Set password to use when logging in.


@dataclass
class GameStatsArguments:
    """Game stats arguments"""
    nodatabase          : bool = False  # Do not use database, and ignore database connection errors.
    nolivetags          : bool = False  # Skip loading unverified tag changes from SQL database. Only load for current user.


@dataclass
class ConfigArguments:
    """Configuration related arguments."""
    englishcoalesced        : bool = False  # Revert to the default (English) coalesced .ini if the language-localized version cannot be found.
    noautoiniupdate         : bool = False  # Suppress prompts to update .ini files.
    noini                   : bool = False  # Do not update the .ini files.
    regenerateinis          : bool = False  # Forces .ini files to be regenerated.

    defeditorini            : str | None = None  # Set the default editor .ini file to use.
    editorini               : str | None = None  # Set the editor .ini file to use.
    defeditorusersettingsini: str | None = None  # Set the default editor user settings .ini file to use.
    editorusersettingsini   : str | None = None  # Set the editor user settings .ini file to use.
    defcompatini            : str | None = None  # Set the default  compatibility .ini file to use.
    compatini               : str | None = None  # Set the compatibility .ini file to use.
    deflightmassini         : str | None = None  # Set the default  lightmass .ini file to use.
    lightmassini            : str | None = None  # Set the lightmass .ini file to use.
    defengineini            : str | None = None  # Set the default  engine .ini file to use.
    engineini               : str | None = None  # Set the engine .ini file to use.
    defgameini              : str | None = None  # Set the default  game .ini file to use.
    gameini                 : str | None = None  # Set the game .ini file to use.
    definputini             : str | None = None  # Set the default  input .ini file to use.
    inputini                : str | None = None  # Set the input .ini file to use.
    defuiini                : str | None = None  # Set the default  UI .ini file to use.
    uiini                   : str | None = None  # Set the UI .ini file to use.


@dataclass
class DebugArguments:
    """Debugging arguments"""
    bugloc          : Vector | None   = None  # (e.g. BugLoc=(X=1798.8569,Y=475.9513,Z=-8.8500))
    bugrot          : Rotation | None = None  # (e.g. BugRot=(Pitch=-1978,Yaw=-7197,Roll=0))


@dataclass
class MiscArguments:
    """Other arguments"""
    timelimit       : float | None = None  # (e.g. timelimit=[time])
    goalscore       : float | None = None  # (e.g. goalscore=[score])
    numbots         : int | None   = None  # (e.g. numbots=[num])


@dataclass
class CLIArguments:
    """Arguments to make the editor run in command line mode."""
    fullstdoutlogoutput : bool = False  # Force all log to be output to stdout.
    utf8output          : bool = False  # Force all output to be UTF-8.
    nullrhi             : bool = False  # Prevent rendering
    warningsaserror     : bool = False  # Treat warnings as errors.


@dataclass
class Arguments:
    """Unreal Editor arguments"""
    # project: str # Path to the pro
    map     : str | None  = None  # Path to the map
    game    : bool = False        # Launch the game
    server  : bool = False        # Launch the game as a server
    address : str | None = None   # Address to connect to

# fmt: on


class Editor(Command):
    """Runs Editor as is. This command exposes a lot of arguments.

    Notes
    -----

    To make your intention clear, you should implement your own Command with a more defined goal.

    Examples
    --------

    .. code-block:: console

       # Launch the uncooked game (no editor, standalone)
       uecli editor RTSGame -game

       # Launch a listen server (Host other clients, 1 local player)
       uecli editor RTSGame /Game/Maps/MyMap?Listen --game

       # Launch a dedicated server (no local players)
       uecli editor RTSGame /Game/Maps/MyMap --server --game --port 8123

       # Launch a client (1 local player)
       uecli editor RTSGame --address localhost --port 8123 --game

    """

    name: str = "editor"

    @staticmethod
    def examples():
        return [
            "uecli editor RTSGame -game",
            "uecli editor RTSGame /Game/Maps/MyMap --server --game --port 8123",
        ]

    @staticmethod
    def arguments(subparsers):
        """Adds the arguments for this command to the given parser"""
        parser = newparser(subparsers, Editor)

        parser.add_argument(
            "--project",
            type=str,
            metavar="project",
            default=None,
            help="Project name, example: <project>.uproject",
        )
        parser.add_argument(
            "--cli",
            action="store_true",
            default=False,
            help="Enable a group of arguments to make the editor as a command line tool",
        )

        parser.add_argument(
            "--dry",
            action="store_true",
            default=False,
            help="Print the command it will execute without running it",
        )
        parser.add_arguments(Arguments, dest="args")
        parser.add_arguments(DevArguments, dest="dev")
        parser.add_arguments(RenderingArguments, dest="rendering")
        parser.add_arguments(NetworkArguments, dest="network")
        parser.add_arguments(UserArguments, dest="user")
        parser.add_arguments(ServerArguments, dest="server")
        parser.add_arguments(GameStatsArguments, dest="stats")
        parser.add_arguments(DebugArguments, dest="debug")
        parser.add_arguments(MiscArguments, dest="misc")

    @staticmethod
    def execute(args):
        if args.cli:
            args.fullstdoutlogoutput = True
            args.utf8output = True
            args.nullrhi = True
            args.warningsaserror = True
            args.nosplash = True
            args.nosound = True
            args.nopause = True
            args.unattended = True

        project = vars(args).pop("project")
        if project is not None and not project.endswith(".uproject"):
            project = find_project(project)

        cmd = [editor_cmd()] + ([project] if project else []) + command_builder(args)
        print(" ".join(cmd))

        if not args.dry:
            fmt = Formatter()
            return popen_with_format(fmt, cmd)

        return 0


COMMANDS = Editor
