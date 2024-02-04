from dataclasses import dataclass

from uetools.core.options import build_mode_choice, platform_choice, projectfield, target_choice


def get(args, name, default=False):
    if hasattr(args, name):
        return getattr(args, name)
    return default


# fmt: off
@dataclass
class BuildCookRunArguments:
    """Build Cook Run UAT arguments"""
    target                                 : str = target_choice()
    config                                 : str = build_mode_choice()
    clientconfig                           : str = build_mode_choice()
    serverconfig                           : str = build_mode_choice()
    platform                               : str = platform_choice()
    # Extracted
    project                                : str = projectfield()   # Project path (required), i.e: -project=QAGame, -project=Samples\BlackJack\BlackJack.uproject, -project=D:\Projects\MyProject.uproject
    destsample                             : bool = False             # Destination Sample name
    foreigndest                            : bool = False             # Foreign Destination
    # targetplatform                         : str  = platform_choice() # target platform for building, cooking and deployment (also -Platform)
    # servertargetplatform                   : str  = platform_choice() # target platform for building, cooking and deployment of the dedicated server (also -ServerPlatform)
    foreign                                : bool = False             # Generate a foreign uproject from blankproject and use that
    foreigncode                            : bool = False             # Generate a foreign code uproject from platformergame and use that
    CrashReporter                          : bool = False             # true if we should build crash reporter
    cook                                   : bool = False             # Determines if the build is going to use cooked data
    cookonthefly                           : bool = False
    skipcook                               : bool = False             # use a cooked build, but we assume the cooked data is up to date and where it belongs, implies -cook
    skipcookonthefly                       : bool = False             # in a cookonthefly build, used solely to pass information to the package step
    clean                                  : bool = False             # wipe intermediate folders before building
    unattended                             : bool = False             # assumes no operator is present, always terminates without waiting for something.
    pak                                    : bool = False             # generate a pak file
    iostore                                : bool = False             # generate I/O store container file(s)
    zenstore                               : bool = False             # save cooked output data to the Zen storage server
    nozenautolaunch                        : bool = False             # URL to a running Zen server
    makebinaryconfig                       : bool = False             # generate optimized config data during staging to improve loadtimes
    signpak                                : str  = None              # sign the generated pak file with the specified key, i.e. -signpak=C:\Encryption.keys. Also implies -signedpak.
    prepak                                 : bool = False             # attempt to avoid cooking and instead pull pak files from the network, implies pak and skipcook
    signed                                 : bool = False             # the game should expect to use a signed pak file.
    PakAlignForMemoryMapping               : bool = False             # The game will be set up for memory mapping bulk data.
    rehydrateassets                        : bool = False             # Should virtualized assets be rehydrated?
    skippak                                : bool = False             # use a pak file, but assume it is already built, implies pak
    skipiostore                            : bool = False             # override the -iostore commandline option to not run it
    stage                                  : bool = False             # put this build in a stage directory
    skipstage                              : bool = False             # uses a stage directory, but assumes everything is already there, implies -stage
    manifests                              : bool = False             # generate streaming install manifests when cooking data
    createchunkinstall                     : bool = False             # generate streaming install data from manifest when cooking data, requires -stage & -manifests
    skipencryption                         : bool = False             # skips encrypting pak files even if crypto keys are provided
    archive                                : bool = False             # put this build in an archive directory
    build                                  : bool = False             # True if build step should be executed
    noxge                                  : bool = False             # True if XGE should NOT be used for building
    CookPartialgc                          : bool = False             # while cooking clean up packages as we are done with them rather then cleaning everything up when we run out of space
    CookInEditor                           : bool = False             # Did we cook in the editor instead of in UAT
    IgnoreCookErrors                       : bool = False             # Ignores cook errors and continues with packaging etc
    nodebuginfo                            : bool = False             # do not copy debug files to the stage
    separatedebuginfo                      : bool = False             # output debug info to a separate directory
    MapFile                                : bool = False             # generates a *.map file
    nocleanstage                           : bool = False             # skip cleaning the stage directory
    run                                    : bool = False             # run the game after it is built (including server, if -server)
    cookonthefly                           : bool = False             # run the client with cooked data provided by cook on the fly server
    Cookontheflystreaming                  : bool = False             # run the client in streaming cook on the fly mode (don't cache files locally instead force reget from server each file load)
    fileserver                             : bool = False             # run the client with cooked data provided by UnrealFileServer
    dedicatedserver                        : bool = False             # build, cook and run both a client and a server (also -server)
    client                                 : bool = False             # build, cook and run a client and a server, uses client target configuration
    noclient                               : bool = False             # do not run the client, just run the server
    logwindow                              : bool = False             # create a log window for the client
    package                                : bool = False             # package the project for the target platform
    skippackage                            : bool = False             # Skips packaging the project for the target platform
    neverpackage                           : bool = False             # Skips preparing data that would be used during packaging, in earlier stages. Different from skippackage which is used to optimize later stages like archive, which still was packaged at some point
    distribution                           : bool = False             # package for distribution the project
    PackageEncryptionKeyFile               : bool = False             # Path to file containing encryption key to use in packaging
    prereqs                                : bool = False             # stage prerequisites along with the project
    applocaldir                            : bool = False             # location of prerequisites for applocal deployment
    Prebuilt                               : bool = False             # this is a prebuilt cooked and packaged build
    AdditionalPackageOptions               : bool = False             # extra options to pass to the platform's packager
    deploy                                 : bool = False             # deploy the project for the target platform
    getfile                                : bool = False             # download file from target after successful run
    IgnoreLightMapErrors                   : bool = False             # Whether Light Map errors should be treated as critical
    trace                                  : bool = False             # The list of trace channels to enable
    tracehost                              : bool = False             # The host address of the trace recorder
    tracefile                              : bool = False             # The file where the trace will be recorded
    sessionlabel                           : bool = False             # A label to pass to analytics
    stagingdirectory                       : str  = None              # Directory to copy the builds to, i.e. -stagingdirectory=C:\Stage
    optionalfilestagingdirectory           : str  = None              # Directory to copy the optional files to, i.e. -optionalfilestagingdirectory=C:\StageOptional
    optionalfileinputdirectory             : str  = None              # Directory to read the optional files from, i.e. -optionalfileinputdirectory=C:\StageOptional
    CookerSupportFilesSubdirectory         : str  = None              # Subdirectory under staging to copy CookerSupportFiles (as set in Build.cs files). -CookerSupportFilesSubdirectory=SDK
    unrealexe                              : str  = None              # Name of the Unreal Editor executable, i.e. -unrealexe=UnrealEditor.exe
    archivedirectory                       : str  = None              # Directory to archive the builds to, i.e. -archivedirectory=C:\Archive
    archivemetadata                        : bool = False             # Archive extra metadata files in addition to the build (e.g. build.properties)
    createappbundle                        : bool = False             # When archiving for Mac, set this to true to package it in a .app bundle instead of normal loose files
    iterativecooking                       : bool = False             # Uses the iterative cooking, command line: -iterativecooking or -iterate
    CookMapsOnly                           : bool = False             # Cook only maps this only affects usage of -cookall the flag
    CookAll                                : bool = False             # Cook all the things in the content directory for this project
    SkipCookingEditorContent               : bool = False             # Skips content under /Engine/Editor when cooking
    FastCook                               : bool = False             # Uses fast cook path if supported by target
    cmdline                                : bool = False             # command line to put into the stage in UECommandLine.txt
    bundlename                             : bool = False             # string to use as the bundle name when deploying to mobile device
    map                                    : bool = False             # map to run the game with
    AdditionalServerMapParams              : bool = False             # Additional server map params, i.e ?param=value
    device                                 : bool = False             # Devices to run the game on
    serverdevice                           : bool = False             # Device to run the server on
    skipserver                             : bool = False             # Skip starting the server
    numclients                             : int  = None              # Start extra clients, n should be 2 or more
    addcmdline                             : bool = False             # Additional command line arguments for the program, which will not be staged in UECommandLine.txt in most cases
    servercmdline                          : bool = False             # Additional command line arguments for the program
    clientcmdline                          : bool = False             # Override command line arguments to pass to the client
    nullrhi                                : bool = False             # add -nullrhi to the client commandlines
    WriteBackMetadataToAssetRegistry       : bool = False             # Passthru to iostore staging, see IoStoreUtilities.cpp
    RetainStagedDirectory                  : bool = False             # If set, retain the staged directory for platforms that modify the I/O store containers for deployment. This is necessary for using the reference container for patch preventing on such platforms.
    fakeclient                             : bool = False             # adds ?fake to the server URL
    editortest                             : bool = False             # rather than running a client, run the editor instead
    RunAutomationTests                     : bool = False             # when running -editortest or a client, run all automation tests, not compatible with -server
    Crash                                  : int  = None              # when running -editortest or a client, adds commands like debug crash, debug rendercrash, etc based on index
    deviceuser                             : bool = False             # Linux username for unattended key genereation
    devicepass                             : bool = False             # Linux password
    RunTimeoutSeconds                      : bool = False             # timeout to wait after we lunch the game
    SpecifiedArchitecture                  : bool = False             # Architecture to use for building any executables (see EditorArchitecture, etc for specific target type control)
    EditorArchitecture                     : bool = False             # Architecture to use for building editor executables
    ServerArchitecture                     : bool = False             # Architecture to use for building server executables
    ClientArchitecture                     : bool = False             # Architecture to use for building client/game executables
    ProgramArchitecture                    : bool = False             # Architecture to use for building program executables
    UbtArgs                                : bool = False             # extra options to pass to ubt
    MapsToRebuildLightMaps                 : bool = False             # List of maps that need light maps rebuilding
    MapsToRebuildHLODMaps                  : bool = False             # List of maps that need HLOD rebuilding
    ForceMonolithic                        : bool = False             # Toggle to combined the result into one executable
    ForceDebugInfo                         : bool = False             # Forces debug info even in development builds
    ForceNonUnity                          : bool = False             # Toggle to disable the unity build system
    ForceUnity                             : bool = False             # Toggle to force enable the unity build system
    Licensee                               : bool = False             #  If set, this build is being compiled by a licensee
    NoSign                                 : bool = False             # Skips signing of code/content files.

    @staticmethod
    def is_server(args):
        return (True or 
            get(args, 'server') or 
            get(args, 'serverconfig') or 
            get(args, 'dedicatedserver') or
            get(args, 'profile') == "server" or
            get(args, "target").endswith("Server")
        )
    
    @staticmethod
    def is_client(args):
        return not BuildCookRunArguments.is_server(args)
# fmt: on
