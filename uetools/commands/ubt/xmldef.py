from dataclasses import dataclass, field


# fmt: off
@dataclass
class BuildConfigurationT:
    bIgnoreOutdatedImportLibraries: bool  = None  #: Whether to ignore import library files that are out of date when building targets. Set this to true to improve iteration time. By default, we do not bother re-linking targets if only a dependent <code>.lib</code> file has changed, as chances are that the import library was not actually different unless a dependent header file of this target was also changed, in which case the target would automatically be rebuilt.
    bPrintDebugInfo               : bool  = None  #: Whether debug info should be written to the console.
    bAllowHybridExecutor          : bool  = None  #: Whether the hybrid executor will be used (a remote executor and local executor).
    bAllowHordeCompute            : bool  = None  #: Whether Horde remote compute may be used. (Highly experimental, disabled by default.)
    bAllowXGE                     : bool  = None  #: Whether XGE may be used.
    bAllowFASTBuild               : bool  = None  #: Whether FASTBuild may be used.
    bAllowSNDBS                   : bool  = None  #: Whether SN-DBS may be used.
    bUseUBTMakefiles              : bool  = None  #: Enables support for very fast iterative builds by caching target data. Turning this on causes Unreal Build Tool (UBT) to emit 'UBT Makefiles' for targets when they are built the first time. Subsequent builds will load these Makefiles and begin outdatedness checking and build invocation very quickly. The caveat is that if source files are added or removed to the project, UBT will need to gather information about those in order for your build to complete successfully. Currently, you must run the project file generator after adding/removing source files to tell UBT to re-gather this information.
    MaxParallelActions            : str   = None  #: Number of actions that can be executed in parallel. If 0 then code will pick a default based on the number of cores and memory available. Applies to the ParallelExecutor, HybridExecutor, and LocalExecutor.
    bAllCores                     : bool  = None  #: Consider logical cores when determining how many total CPU cores are available.
    bCompactOutput                : bool  = None  #: Instruct the executor to write compact output (for example, only errors), if supported by the executor. This field is used to hold the value when specified from the command line or XML.
    bDebugBuildsActuallyUseDebugCRT: bool  = None  #: Enables the debug C++ runtime (CRT) for debug builds. By default we always use the release runtime, since the debug version isn't particularly useful when debugging Unreal Engine projects, and linking against the debug CRT libraries forces our third party library dependencies to also be compiled using the debug CRT (and often perform more slowly). Often it can be inconvenient to require a separate copy of the debug versions of third party static libraries simply so that you can debug your program's code.
    bLegalToDistributeBinary      : bool  = None  #: Whether the output from this target can be publicly distributed, even if it has dependencies on modules that are in folders with special restrictions (for example, CarefullyRedist, NotForLicensees, NoRedist).
    bUseInlining                  : bool  = None  #: Enable inlining for all modules.
    bUseDebugLiveCodingConsole    : bool  = None  #: Whether to enable support for live coding.
    bUseXGEController             : bool  = None  #: Whether the XGE controller worker and modules should be included in the engine build. These are required for distributed shader compilation using the XGE interception interface.
    bUseUnityBuild                : bool  = None  #: Whether to unify C++ code into larger files for faster compilation.
    bForceUnityBuild              : bool  = None  #: Whether to force C++ source files to be combined into larger files for faster compilation.
    bMergeModuleAndGeneratedUnityFiles: bool  = None  #: Whether to merge the module and generated unity files for faster compilation.
    bUseAdaptiveUnityBuild        : bool  = None  #: Use a heuristic to determine which files are currently being iterated on and exclude them from unity blobs, resulting in faster incremental compile times. The current implementation uses the read-only flag to distinguish the working set, assuming that files will be made writable by the source control system if they are being modified. This is true for Perforce, but not for Git.
    bAdaptiveUnityDisablesOptimizations: bool  = None  #: Disable optimization for files that are in the adaptive non-unity working set.
    bAdaptiveUnityDisablesPCH     : bool  = None  #: Disables force-included Precompiled Headers (PCHs) for files that are in the adaptive non-unity working set.
    bAdaptiveUnityDisablesProjectPCHForProjectPrivate: bool  = None  #: Backing storage for <code>bAdaptiveUnityDisablesProjectPCH</code>.
    bAdaptiveUnityCreatesDedicatedPCH: bool  = None  #: Creates a dedicated PCH for each source file in the working set, allowing faster iteration on cpp-only changes.
    bAdaptiveUnityEnablesEditAndContinue: bool  = None  #: Creates a dedicated PCH for each source file in the working set, allowing faster iteration on cpp-only changes.
    bAdaptiveUnityCompilesHeaderFiles: bool  = None  #: Creates a dedicated source file for each header file in the working set to detect missing includes in headers.
    MinGameModuleSourceFilesForUnityBuild: str   = None  #: The number of source files in a game module before unity build will be activated for that module.  This allows small game modules to have faster iterative compile times for single files, at the expense of slower full rebuild times.  This setting can be overridden by the <code>bFasterWithoutUnity</code> option in a module's <code>.Build.cs</code> file.
    DefaultWarningLevel           : str   = None  #: Default treatment of uncategorized warnings
    DeprecationWarningLevel       : str   = None  #: Level to report deprecation warnings as errors
    bWarningsAsErrors             : bool  = None  #: Whether to enable all warnings as errors. UE enables most warnings as errors already, but disables a few (such as deprecation warnings).
    UnsafeTypeCastWarningLevel    : str   = None  #: Indicates what warning/error level to treat unsafe type casts as on platforms that support it (for example, <code>double-&gt;float</code> or <code>int64-&gt;int32</code>).
    bUndefinedIdentifierErrors    : bool  = None  #: Forces the use of undefined identifiers in conditional expressions to be treated as errors.
    bRetainFramePointers          : bool  = None  #: Forces frame pointers to be retained. This is usually required when you want reliable callstacks (for example, <code>mallocframeprofiler</code>).
    bUseFastMonoCalls             : bool  = None  #: New Monolithic Graphics drivers have optional "fast calls" replacing various D3d functions.
    NumIncludedBytesPerUnityCPP   : str   = None  #: An approximate number of bytes of C++ code to target for inclusion in a single unified C++ file.
    bStressTestUnity              : bool  = None  #: Whether to stress test the C++ unity build robustness by including all C++ files files in a project from a single unified file.
    bDetailedUnityFiles           : bool  = None  #: Whether to add additional information to the unity files, such as '_of_X' in the file name.
    bDisableDebugInfo             : bool  = None  #: Whether to globally disable debug info generation; see <code>DebugInfoHeuristics.cs</code> for per-config and per-platform options.
    bDisableDebugInfoForGeneratedCode: bool  = None  #: Whether to disable debug info generation for generated files. This improves link times for modules that have a lot of generated glue code.
    bOmitPCDebugInfoInDevelopment : bool  = None  #: Whether to disable debug info on PC/Mac in development builds (for faster developer iteration, as link times are extremely fast with debug info disabled).
    bUsePDBFiles                  : bool  = None  #: Whether PDB files should be used for Visual C++ builds.
    bUsePCHFiles                  : bool  = None  #: Whether PCH files should be used.
    bDeterministic                : bool  = None  #: Set flags required for deterministic linking (experimental, may not be fully supported). Deterministic compiling is controlled via <code>ModuleRules.cs</code>.
    bForceDeterministic           : bool  = None  #: Force set flags required for deterministic compiling and linking (experimental, may not be fully supported). This setting is only recommended for testing, instead:
    bPreprocessDepends            : bool  = None  #: Generate dependency files by preprocessing. This is only recommended when distributing builds as it adds additional overhead.
    StaticAnalyzer                : str   = None  #: Whether static code analysis should be enabled.
    StaticAnalyzerOutputType      : str   = None  #: The output type to use for the static analyzer. This is only supported for Clang.
    StaticAnalyzerMode            : str   = None  #: The mode to use for the static analyzer. This is only supported for Clang. Shallow mode completes quicker but is generally not recommended.
    MinFilesUsingPrecompiledHeader: str   = None  #: The minimum number of files that must use a pre-compiled header before it will be created and used.
    bForcePrecompiledHeaderForGameModules: bool  = None  #: When enabled, a precompiled header is always generated for game modules, even if there are only a few source files in the module.  This greatly improves compile times for iterative changes on a few files in the project, at the expense of slower full rebuild times for small game projects.  This can be overridden by setting <code>MinFilesUsingPrecompiledHeaderOverride</code> in a module's <code>Build.cs</code> file.
    bUseIncrementalLinking        : bool  = None  #: Whether to use incremental linking or not. Incremental linking can yield faster iteration times when making small changes. Currently disabled by default because it tends to behave a bit buggy on some computers (PDB-related compile errors).
    bAllowLTCG                    : bool  = None  #: Whether to allow the use of link time code generation (LTCG).
    bPreferThinLTO                : bool  = None  #: When Link Time Code Generation (LTCG) is enabled, whether to prefer using the lighter weight version on supported platforms.
    bPGOProfile                   : bool  = None  #: Whether to enable Profile Guided Optimization (PGO) instrumentation in this build.
    bPGOOptimize                  : bool  = None  #: Whether to optimize this build with Profile Guided Optimization (PGO).
    bSupportEditAndContinue       : bool  = None  #: Whether to support edit and continue.  Only works on Microsoft compilers.
    bOmitFramePointers            : bool  = None  #: Whether to omit frame pointers or not. Disabling is useful, for example, for memory profiling on the PC.
    bUseMallocProfiler            : bool  = None  #: If true, then enable memory profiling in the build (defines <code>USE_MALLOC_PROFILER=1</code> and forces <code>bOmitFramePointers=false</code>).
    bUseSharedPCHs                : bool  = None  #: Enables "Shared PCHs", a feature which significantly speeds up compile times by attempting to share certain PCH files between modules that UBT detects are including those PCH's header files.
    bUseShippingPhysXLibraries    : bool  = None  #: True if Development and Release builds should use the release configuration of PhysX/APEX.
    bUseCheckedPhysXLibraries     : bool  = None  #: True if Development and Release builds should use the checked configuration of PhysX/APEX. if <code>bUseShippingPhysXLibraries</code> is true this is ignored.
    bCheckLicenseViolations       : bool  = None  #: Tells the UBT to check if the module currently being built is violating EULA.
    bBreakBuildOnLicenseViolation : bool  = None  #: Tells the UBT to break build if the module currently being built is violating EULA.
    bUseFastPDBLinking            : bool  = None  #: Whether to use the <code>:FASTLINK</code> option when building with /DEBUG to create local PDBs on Windows. Fast, but currently seems to have problems finding symbols in the debugger.
    bCreateMapFile                : bool  = None  #: Outputs a map file as part of the build.
    bAllowRuntimeSymbolFiles      : bool  = None  #: True if runtime symbols files should be generated as a post build step for some platforms. These files are used by the engine to resolve symbol names of callstack backtraces in logs.
    PackagePath                   : str   = None  #: Package full path (directory + filename) where to store input files used at link time. Normally used to debug a linker crash for platforms that support it.
    CrashDiagnosticDirectory      : str   = None  #: Directory where to put crash report files for platforms that support it.
    bCheckSystemHeadersForModification: bool  = None  #: Whether headers in system paths should be checked for modification when determining outdated actions.
    bFlushBuildDirOnRemoteMac     : bool  = None  #: Whether to clean <code>Builds</code> directory on a remote Mac before building.
    bPrintToolChainTimingInfo     : bool  = None  #: Whether to write detailed timing info from the compiler and linker.
    bParseTimingInfoForTracing    : bool  = None  #: Whether to parse timing data into a tracing file compatible with <code>chrome://tracing</code>.
    bPublicSymbolsByDefault       : bool  = None  #: Whether to expose all symbols as public by default on POSIX platforms.
    CppStandard                   : str   = None  #: Which C++ standard to use for compiling this target.
    CStandard                     : str   = None  #: Which C standard to use for compiling this target.
    bStopSNDBSCompilationAfterErrors: bool  = None  #: When enabled, SN-DBS will stop compiling targets after a compile error occurs.  Recommended, as it saves computing resources for others.
    bXGENoWatchdogThread          : bool  = None  #: Whether to use the <code>no_watchdog_thread</code> option to prevent VS2015 toolchain stalls.
    bShowXGEMonitor               : bool  = None  #: Whether to display the XGE build monitor.
    bStopXGECompilationAfterErrors: bool  = None  #: When enabled, XGE will stop compiling targets after a compile error occurs.  Recommended, as it saves computing resources for others.
    BaseLogFileName               : str   = None  #: Specifies the file to use for logging.
    bStripSymbols                 : bool  = None  #: Whether to strip iOS symbols or not (implied by Shipping config).
    bEnableAddressSanitizer       : bool  = None  #: Enables address sanitizer (ASan). Only supported for Visual Studio 2019 16.7.0 and up.
    bEnableThreadSanitizer        : bool  = None  #: Enables thread sanitizer (TSan).
    bEnableUndefinedBehaviorSanitizer: bool  = None  #: Enables undefined behavior sanitizer (UBSan).
    bEnableMemorySanitizer        : bool  = None  #: Enables memory sanitizer (MSan).
    bTuneDebugInfoForLLDB         : bool  = None  #: Turns on tuning of debug info for LLDB.
    bUseDSYMFiles                 : bool  = None  #: Enables the generation of <code>.dsym</code> files. This can be disabled to enable faster iteration times during development.
    bWriteSolutionOptionFile      : bool  = None  #: Whether to write a solution option (suo) file for the <code>.sln</code>.
    bVsConfigFile                 : bool  = None  #: Whether to write a .vsconfig file next to the sln to suggest components to install.
    bAddFastPDBToProjects         : bool  = None  #: Whether to add the <code>-FastPDB</code> option to build command lines by default.
    bUsePerFileIntellisense       : bool  = None  #: Whether to generate per-file intellisense data.
    bEditorDependsOnShaderCompileWorker: bool  = None  #: Whether to include a dependency on ShaderCompileWorker when generating project files for the editor.


@dataclass
class UEBuildConfigurationT:
    bForceHeaderGeneration        : bool  = None  #: If true, force header regeneration. Intended for the build machine.
    bDoNotBuildUHT                : bool  = None  #: If true, do not build Unreal Header Tool (UHT), assume it is already built.
    bFailIfGeneratedCodeChanges   : bool  = None  #: If true, fail if any of the generated header files is out of date.
    bAllowHotReloadFromIDE        : bool  = None  #: True if hot-reload from IDE is allowed.
    bForceDebugUnrealHeaderTool   : bool  = None  #: If true, the Debug version of Unreal Header Tool (UHT) will be built and run instead of the Development version.
    bUseBuiltInUnrealHeaderTool   : bool  = None  #: If true, use Unreal Header Tool (UHT) internal to Unreal Build Tool (UBT).


@dataclass
class WindowsPlatformT:
    MaxRootPathLength             : str   = None  #: Maximum recommended root path length.
    MaxNestedPathLength           : str   = None  #: Maximum length of a path relative to the root directory. Used on Windows to ensure paths are portable between machines. Defaults to off.
    Compiler                      : str   = None  #: Version of the compiler toolchain to use on Windows platform. A value of "default" will be changed to a specific version at UBT start up.
    CompilerVersion               : str   = None  #: The specific toolchain version to use. This may be a specific version number (for example, "14.13.26128"), the string "Latest" to select the newest available version, or the string "Preview" to select the newest available preview version. By default, and if it is available, we use the toolchain version indicated by <code>WindowsPlatform.DefaultToolChainVersion</code> (otherwise, we use the latest version).
    WindowsSdkVersion             : str   = None  #: The specific Windows SDK version to use. This may be a specific version number (for example, "8.1", "10.0" or "10.0.10150.0"), or the string "Latest", to select the newest available version. By default, and if it is available, we use the Windows SDK version indicated by <code>WindowsPlatform.DefaultWindowsSdkVersion</code> (otherwise, we use the latest version).
    StaticAnalyzer                : str   = None  #: The static analyzer to use.
    StaticAnalyzerOutputType      : str   = None  #: The output type to use for the static analyzer.
    bStrictConformanceMode        : bool  = None  #: Enables strict standard conformance mode (/permissive-) in Visual Studio 2017 or higher.
    PCHMemoryAllocationFactor     : str   = None  #: Determines the amount of memory that the compiler allocates to construct precompiled headers (/Zm).
    AdditionalLinkerOptions       : str   = None  #: Allow the target to specify extra options for linking that are not otherwise noted here.
    bClangTimeTrace               : bool  = None  #: (Experimental) Appends the -ftime-trace argument to the command line for Clang to output a JSON file containing a timeline for the compile. See the <a id="content_link" href="http://aras-p.info/blog/2019/01/16/time-trace-timeline-flame-chart-profiler-for-Clang/"><span>Clang Time Trace</span></a> documentation for more info.
    bCompilerTrace                : bool  = None  #: Outputs compile timing information so that it can be analyzed.
    bShowIncludes                 : bool  = None  #: Print out files that are included by each source file.


@dataclass
class ModuleConfigurationT:
    DisableUnityBuild             : str   = None  #: List of modules for which to disable unity builds.
    EnableOptimizeCode            : str   = None  #: List of modules for which to enable optimizations.
    DisableOptimizeCode           : str   = None  #: List of modules for which to disable optimizations.


@dataclass
class FASTBuildT:
    FBuildExecutablePath          : str   = None  #: Used to specify the location of <code>fbuild.exe</code> if the distributed binary isn't being used.
    bEnableDistribution           : bool  = None  #: Controls network build distribution.
    FBuildBrokeragePath           : str   = None  #: Used to specify the location of the brokerage. If null, <code>FASTBuild</code> will fall back to checking <code>FASTBUILD_BROKERAGE_PATH</code>.
    FBuildCoordinator             : str   = None  #: Used to specify the <code>FASTBuild</code> coordinator IP or network name. If null, <code>FASTBuild</code> will fall back to checking <code>FASTBUILD_COORDINATOR</code>.
    bEnableCaching                : bool  = None  #: Controls whether to use caching at all. <code>CachePath</code> and <code>FASTCacheMode</code> are only relevant if this is enabled.
    CacheMode                     : str   = None  #: Cache access mode - only relevant if <code>bEnableCaching</code> is true.
    FBuildCachePath               : str   = None  #: Used to specify the location of the cache. If null, <code>FASTBuild</code> will fall back to checking <code>FASTBUILD_CACHE_PATH</code>.
    bForceRemote                  : bool  = None  #: Whether to force remote.
    bStopOnError                  : bool  = None  #: Whether to stop on error.
    MsvcCRTRedistVersion          : str   = None  #: Which Microsoft Visual C++ (MSVC) C++ Runtime (CRT) Redist version to use.


@dataclass
class HordeExecutorT:
    NumRemoteParallelProcesses    : str   = None  #: How many processes that will be executed in parallel remotely.
    RemoteProcessOnly             : str   = None  #: Only run work remotely, for testing.
    RetryFailedRemote             : str   = None  #: Retry actions locally when failed remotely.


@dataclass
class ParallelExecutorT:
    MaxProcessorCount             : str   = None  #: Maximum processor count for local execution.
    ProcessorCountMultiplier      : str   = None  #: Processor count multiplier for local execution. Can be below 1 to reserve CPU for other tasks. When using the local executor (not XGE), run a single action on each CPU core. Note that you can set this to a larger value to get slightly faster build times in many cases, but your computer's responsiveness during compiling may be much worse. This value is ignored if the CPU does not support hyper-threading.
    MemoryPerActionBytes          : str   = None  #: Free memory per action in bytes, used to limit the number of parallel actions if the machine is memory starved. Set to 0 to disable free memory checking.
    ProcessPriority               : str   = None  #: The priority to set for spawned processes. Valid Settings: <code>Idle</code>, <code>BelowNormal</code>, <code>Normal</code>, <code>AboveNormal</code>, <code>High</code>. Default Setting: <code>BelowNormal</code>.
    bStopCompilationAfterErrors   : bool  = None  #: When enabled, will stop compiling targets after a compile error occurs.
    bShowCompilationTimes         : bool  = None  #: Whether to show compilation times along with the worst offenders or not.
    bShowPerActionCompilationTimes: bool  = None  #: Whether to show compilation times for each executed action.
    bLogActionCommandLines        : bool  = None  #: Whether to log command lines for actions being executed.
    bPrintActionTargetNames       : bool  = None  #: Add target names for each action executed.


@dataclass
class SNDBST:
    bAllowOverVpn                 : bool  = None  #: When set to false, SNDBS will not be enabled when running connected to the coordinator over VPN. Configure VPN-assigned subnets via the VpnSubnets parameter.
    VpnSubnets                    : str   = None  #: List of subnets containing IP addresses assigned by VPN.


@dataclass
class XGET:
    bAllowOverVpn                 : bool  = None  #: When set to false, XGE will not be enabled when running connected to the coordinator over VPN. Configure VPN-assigned subnets via the VpnSubnets parameter.
    VpnSubnets                    : str   = None  #: List of subnets containing IP addresses assigned by VPN.
    bAllowRemoteLinking           : bool  = None  #: Whether to allow remote linking.
    bUseVCCompilerMode            : bool  = None  #: Whether to enable the <code>VCCompiler=true</code> setting. This requires an additional license for VC tools.
    MinActions                    : str   = None  #: Minimum number of actions to use XGE execution.
    bUnavailableIfInUse           : bool  = None  #: Check for a concurrent XGE build and treat the XGE executor as unavailable if it's in use. This will allow UBT to fall back to another executor such as the parallel executor.


@dataclass
class BuildModeT:
    bIgnoreJunk                   : bool  = None  #: Whether to skip checking for files identified by the junk manifest.


@dataclass
class ProjectFileGeneratorT:
    DisablePlatformProjectGenerators: str   = None  #: Disable native project file generators for platforms. Platforms with native project file generators typically require IDE extensions to be installed.
    Format                        : str   = None  #: Default list of project file formats to generate.
    bGenerateIntelliSenseData     : bool  = None  #: True if intellisense data should be generated (takes a while longer).
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bAllDocumentationLanguages    : bool  = None  #: True if all documentation languages should be included in generated projects, otherwise only INT files will be included.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeBuildSystemFiles      : bool  = None  #: True if build system files should be included.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeLocalizationFiles     : bool  = None  #: True if we should include localization files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass <code>-DotNet</code> to enable this.
    bIncludeTempTargets           : bool  = None  #: Whether to include temporary targets generated by Unreal Automation Tool (UAT) to support content only projects with non-default settings.
    bKeepSourceSubDirectories     : bool  = None  #: True if we should reflect <code>Source</code> sub-directories on disk in the primary project as project directories. This adds some visual clutter to the primary project but it is truer to the on-disk file organization.
    Platforms                     : str   = None  #: Names of platforms to include in the generated project files.
    Configurations                : str   = None  #: Names of configurations to include in the generated project files. See <code>UnrealTargetConfiguration</code> for valid entries.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.
    bIncludeTestAndShippingConfigs: bool  = None  #: Whether we should include configurations for "Test" and "Shipping" in generated projects. Pass <code>-NoShippingConfigs</code> to disable this.
    bIncludeDebugConfigs          : bool  = None  #: Whether we should include configurations for "Debug" and "DebugGame" in generated projects. Pass <code>-NoDebugConfigs</code> to disable this.
    bIncludeDevelopmentConfigs    : bool  = None  #: Whether we should include configurations for "Development" in generated projects. Pass <code>-NoDevelopmentConfigs</code> to disable this.


@dataclass
class IOSToolChainT:
    IOSSDKVersion                 : str   = None  #: The version of the iOS SDK to target at build time.
    BuildIOSVersion               : str   = None  #: The version of the iOS to allow at build time.
    bUseDangerouslyFastMode       : bool  = None  #: If this is set, then we do not do any post-compile steps - except moving the executable into the proper spot on Mac.


@dataclass
class WindowsTargetRulesT:
    ObjSrcMapFile                 : str   = None  #: Whether we should export a file containing <code>.obj</code> to source file mappings.


@dataclass
class CLionGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass <code>-DotNet</code> to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class CMakefileGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass <code>-DotNet</code> to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class CodeLiteGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include C# program projects in the generated solution. Pass <code>-DotNet</code> to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class EddieProjectFileGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass "-DotNet" to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class KDevelopGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass "-DotNet" to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class MakefileGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass "-DotNet" to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class QMakefileGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass "-DotNet" to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class RiderProjectFileGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass "-DotNet" to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class VSCodeProjectFileGeneratorT:
    IncludeAllFiles               : str   = None  #: Includes all files in the generated workspace.
    AddDebugAttachConfig          : str   = None  #: Whether VS Code project generation should include debug configurations to allow attaching to already running processes
    AddDebugCoreConfig            : str   = None  #: Whether VS Code project generation should include debug configurations to allow core dump debugging
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass "-DotNet" to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class VCMacProjectFileGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass "-DotNet" to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class VCProjectFileGeneratorT:
    Version                       : str   = None  #: The version of Visual Studio to generate project files for.
    MaxSharedIncludePaths         : str   = None  #: Puts the most common include paths in the <code>IncludePath</code> property in the <code>MSBuild</code> project. This significantly reduces Visual Studio memory usage (measured <code>1.1GB -&gt; 500mb</code>), but seems to be causing issues with Visual Assist. Value here specifies maximum length of the include path list in KB.
    ExcludedIncludePaths          : str   = None  #: Semi-colon separated list of paths that should not be added to the projects include paths. Useful for omitting third-party headers (for example, <code>ThirdParty/WebRTC</code>) from intellisense suggestions and reducing memory footprints.
    ExcludedFilePaths             : str   = None  #: Semi-colon separated list of paths that should not be added to the projects. Useful for omitting third-party files (for example, <code>ThirdParty/WebRTC</code>) from intellisense suggestions and reducing memory footprints.
    bBuildUBTInDebug              : bool  = None  #: Forces Unreal Build Tool (UBT) to be built in debug configuration, regardless of the solution configuration.
    bBuildLiveCodingConsole       : bool  = None  #: Whether to include a dependency on <code>LiveCodingConsole</code> when building targets that support live coding.
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the <code>-useprecompiled</code> argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (<code>.ini</code>) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets.
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass "-DotNet" to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class XcodeProjectFileGeneratorT:
    bIncludeDocumentation         : bool  = None  #: True if we should include documentation in the generated projects.
    bUsePrecompiled               : bool  = None  #: True if build targets should pass the -useprecompiled argument.
    bIncludeEngineSource          : bool  = None  #: True if we should include engine source in the generated solution.
    bIncludeShaderSource          : bool  = None  #: True if shader source files should be included in generated projects.
    bIncludeConfigFiles           : bool  = None  #: True if we should include config (.ini) files in the generated project.
    bIncludeTemplateFiles         : bool  = None  #: True if we should include template files in the generated project.
    bIncludeEnginePrograms        : bool  = None  #: True if we should include program projects in the generated solution.
    IncludeCppSource              : str   = None  #: Whether to include C++ targets
    bIncludeDotNetPrograms        : bool  = None  #: True if we should include csharp program projects in the generated solution. Pass <code>-DotNet</code> to enable this.
    PrimaryProjectName            : str   = None  #: Name of the primary project file - for example, the base file name for the Visual Studio solution file, or the Xcode project file on Mac.
    bPrimaryProjectNameFromFolder : bool  = None  #: If true, sets the primary project name according to the name of the folder it is in.


@dataclass
class SourceFileWorkingSetT:
    Provider                      : str   = None  #: Sets the provider to use for determining the working set.
    RepositoryPath                : str   = None  #: Sets the path to use for the repository. Interpreted relative to the Unreal Engine root directory (the folder above the <code>Engine</code> folder) - if relative.
    GitPath                       : str   = None  #: Sets the path to use for the Git executable. Defaults to "git" (assuming it is in the <code>PATH</code>).


@dataclass
class RemoteMacT:
    ServerName                    : str   = None  #: These two variables will be loaded from the XML config file in <code>XmlConfigLoader.Init()</code>.
    UserName                      : str   = None  #: The remote username.
    SshPrivateKey                 : str   = None  #: If set, instead of looking for <code>RemoteToolChainPrivate.key</code> in the usual places (<code>Documents/Unreal</code>, <code>Engine/UnrealBuildTool/SSHKeys</code> or <code>Engine/Build/SSHKeys</code>), this private key will be used.
    RsyncAuthentication           : str   = None  #: The authentication used for Rsync (for the -e rsync flag).
    SshAuthentication             : str   = None  #: The authentication used for SSH (similar to RsyncAuthentication).


@dataclass
class HoloLensPlatformT:
    Compiler                      : str   = None  #: Version of the compiler toolchain to use on HoloLens. A value of "default" will be changed to a specific version at UBT startup.


@dataclass
class LogT:
    bBackupLogFiles               : bool  = None  #: Whether to backup an existing log file, rather than overwriting it.
    LogFileBackupCount            : str   = None  #: The number of log file backups to preserve. Older backups will be deleted.


@dataclass
class Configuration:
    BuildConfiguration            : BuildConfigurationT            = field(default_factory=BuildConfigurationT)
    UEBuildConfiguration          : UEBuildConfigurationT          = field(default_factory=UEBuildConfigurationT)
    WindowsPlatform               : WindowsPlatformT               = field(default_factory=WindowsPlatformT)
    ModuleConfiguration           : ModuleConfigurationT           = field(default_factory=ModuleConfigurationT)
    FASTBuild                     : FASTBuildT                     = field(default_factory=FASTBuildT)
    HordeExecutor                 : HordeExecutorT                 = field(default_factory=HordeExecutorT)
    ParallelExecutor              : ParallelExecutorT              = field(default_factory=ParallelExecutorT)
    SNDBS                         : SNDBST                         = field(default_factory=SNDBST)
    XGE                           : XGET                           = field(default_factory=XGET)
    BuildMode                     : BuildModeT                     = field(default_factory=BuildModeT)
    ProjectFileGenerator          : ProjectFileGeneratorT          = field(default_factory=ProjectFileGeneratorT)
    IOSToolChain                  : IOSToolChainT                  = field(default_factory=IOSToolChainT)
    WindowsTargetRules            : WindowsTargetRulesT            = field(default_factory=WindowsTargetRulesT)
    CLionGenerator                : CLionGeneratorT                = field(default_factory=CLionGeneratorT)
    CMakefileGenerator            : CMakefileGeneratorT            = field(default_factory=CMakefileGeneratorT)
    CodeLiteGenerator             : CodeLiteGeneratorT             = field(default_factory=CodeLiteGeneratorT)
    EddieProjectFileGenerator     : EddieProjectFileGeneratorT     = field(default_factory=EddieProjectFileGeneratorT)
    KDevelopGenerator             : KDevelopGeneratorT             = field(default_factory=KDevelopGeneratorT)
    MakefileGenerator             : MakefileGeneratorT             = field(default_factory=MakefileGeneratorT)
    QMakefileGenerator            : QMakefileGeneratorT            = field(default_factory=QMakefileGeneratorT)
    RiderProjectFileGenerator     : RiderProjectFileGeneratorT     = field(default_factory=RiderProjectFileGeneratorT)
    VSCodeProjectFileGenerator    : VSCodeProjectFileGeneratorT    = field(default_factory=VSCodeProjectFileGeneratorT)
    VCMacProjectFileGenerator     : VCMacProjectFileGeneratorT     = field(default_factory=VCMacProjectFileGeneratorT)
    VCProjectFileGenerator        : VCProjectFileGeneratorT        = field(default_factory=VCProjectFileGeneratorT)
    XcodeProjectFileGenerator     : XcodeProjectFileGeneratorT     = field(default_factory=XcodeProjectFileGeneratorT)
    SourceFileWorkingSet          : SourceFileWorkingSetT          = field(default_factory=SourceFileWorkingSetT)
    RemoteMac                     : RemoteMacT                     = field(default_factory=RemoteMacT)
    HoloLensPlatform              : HoloLensPlatformT              = field(default_factory=HoloLensPlatformT)
    Log                           : LogT                           = field(default_factory=LogT)
# fmt: on
