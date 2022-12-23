import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from uetools.core.command import Command, newparser
from uetools.core.conf import engine_folder, find_project

valid_file = """
<?xml version="1.0" encoding="utf-8" ?>
<Configuration xmlns="https://www.unrealengine.com/BuildConfiguration">
    <ParallelExecutor>
        <MaxProcessorCount>32</MaxProcessorCount>
    </ParallelExecutor>
    <BuildConfiguration>
    </BuildConfiguration>
    <WindowsPlatform>
    </WindowsPlatform>
</Configuration>
"""


# Can I make a Dataclass of the UBT config and initialize it using the XML
# and save the XML from the dataclass ?
# 100% it is possible, just might take some time
# I can just save the dataclass as a dict and save the values as
#
# <dict>
#   <key>value</key>
# </dict>


@dataclass
class WindowsPlatform:
    pass


@dataclass
class ModuleConfiguration:
    pass


@dataclass
class FASTBuild:
    pass


@dataclass
class TaskExecutor:
    pass


@dataclass
class HybridExecutor:
    pass


@dataclass
class ParallelExecutor:
    bStopCompilationAfterErrors: bool = False
    bShowCompilationTimes: bool = False
    bShowPerActionCompilationTimes: bool = True
    bLogActionCommandLines: bool = True
    bPrintActionTargetNames: bool = True
    MaxProcessorCount: int = 32
    ProcessorCountMultiplier: float = 1
    MemoryPerActionBytes: int = 0


@dataclass
class SNDBS:
    pass


@dataclass
class XGE:
    pass


@dataclass
class BuildMode:
    pass


@dataclass
class ProjectFileGenerator:
    pass


@dataclass
class HoloLensPlatform:
    pass


@dataclass
class IOSToolChain:
    pass


@dataclass
class WindowsTargetRules:
    pass


@dataclass
class CLionGenerator:
    pass


@dataclass
class CMakeFileGenerator:
    pass


@dataclass
class CodeLiteGenerator:
    pass


@dataclass
class EddieProjectFileGenerator:
    pass


@dataclass
class KDevelopGenerator:
    pass


@dataclass
class MakefileGenerator:
    pass


@dataclass
class QMakefileGenerator:
    pass


@dataclass
class RiderProjectGenerator:
    pass


@dataclass
class VSCodeProjectFileGenerator:
    pass


@dataclass
class VCMakeProjectFileGenerator:
    pass


@dataclass
class VCProjetFileGenerator:
    pass


@dataclass
class XCodeProjectFileGenerator:
    pass


@dataclass
class SourceFileWorkingSet:
    pass


@dataclass
class RemoteMac:
    pass


@dataclass
class Log:
    pass


@dataclass
class Configuration:
    WindowsPlatform: WindowsPlatform = field(default_factory=WindowsPlatform)
    ModuleConfiguration: ModuleConfiguration = field(
        default_factory=ModuleConfiguration
    )
    FASTBuild: FASTBuild = field(default_factory=FASTBuild)
    TaskExecutor: TaskExecutor = field(default_factory=TaskExecutor)
    HybridExecutor: HybridExecutor = field(default_factory=HybridExecutor)
    ParallelExecutor: ParallelExecutor = field(default_factory=ParallelExecutor)
    SNDBS: SNDBS = field(default_factory=SNDBS)
    XGE: XGE = field(default_factory=XGE)
    BuildMode: BuildMode = field(default_factory=BuildMode)
    ProjectFileGenerator: ProjectFileGenerator = field(
        default_factory=ProjectFileGenerator
    )
    HoloLensPlatform: HoloLensPlatform = field(default_factory=HoloLensPlatform)
    IOSToolChain: IOSToolChain = field(default_factory=IOSToolChain)
    WindowsTargetRules: WindowsTargetRules = field(default_factory=WindowsTargetRules)
    CLionGenerator: CLionGenerator = field(default_factory=CLionGenerator)
    CMakeFileGenerator: CMakeFileGenerator = field(default_factory=CMakeFileGenerator)
    CodeLiteGenerator: CodeLiteGenerator = field(default_factory=CodeLiteGenerator)
    EddieProjectFileGenerator: EddieProjectFileGenerator = field(
        default_factory=EddieProjectFileGenerator
    )
    KDevelopGenerator: KDevelopGenerator = field(default_factory=KDevelopGenerator)
    MakefileGenerator: MakefileGenerator = field(default_factory=MakefileGenerator)
    QMakefileGenerator: QMakefileGenerator = field(default_factory=QMakefileGenerator)
    RiderProjectGenerator: RiderProjectGenerator = field(
        default_factory=RiderProjectGenerator
    )
    VSCodeProjectFileGenerator: VSCodeProjectFileGenerator = field(
        default_factory=VSCodeProjectFileGenerator
    )
    VCMakeProjectFileGenerator: VCMakeProjectFileGenerator = field(
        default_factory=VCMakeProjectFileGenerator
    )
    VCProjetFileGenerator: VCProjetFileGenerator = field(
        default_factory=VCProjetFileGenerator
    )
    XCodeProjectFileGenerator: XCodeProjectFileGenerator = field(
        default_factory=XCodeProjectFileGenerator
    )
    SourceFileWorkingSet: SourceFileWorkingSet = field(
        default_factory=SourceFileWorkingSet
    )
    RemoteMac: RemoteMac = field(default_factory=RemoteMac)
    Log: Log = field(default_factory=Log)


class LimitCPU(Command):
    """Disable unused plugin that are loading by default"""

    name: str = "limitcpu"

    @staticmethod
    def arguments(subparsers):
        parser = newparser(subparsers, LimitCPU)
        parser.add_argument(
            "--cpu", default=32, type=int, help="Limit the number of cpu to use"
        )

    @staticmethod
    def execute(args):
        #
        # https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/DevelopmentSetup/BuildConfigurations/
        # https://docs.unrealengine.com/5.0/en-US/build-configuration-for-unreal-engine/
        #
        engine = engine_folder()
        namespaces = {"ue": "https://www.unrealengine.com/BuildConfiguration"}
        global_ubt_config = os.path.join(
            engine, "Saved", "UnrealBuildTool", "BuildConfiguration.xml"
        )
        # user_ubt_config = os.path.join(home, "AppData", "Roaming", "Unreal Engine", "UnrealBuildTool", "BuildConfiguration.xml")
        # local_ubt_config = os.path.join(home, "Documents", "Unreal Engine", "UnrealBuildTool", "BuildConfiguration.xml")

        ET.register_namespace("", "https://www.unrealengine.com/BuildConfiguration")
        tree = ET.parse(global_ubt_config)

        root = tree.getroot()

        val = root.find("ue:ParallelExecutor/ue:MaxProcessorCount", namespaces)
        oldval = val.text
        val.text = str(args.cpu)

        print(f"CPU {oldval} => {args.cpu}")
        tree.write(global_ubt_config, xml_declaration=True, encoding="utf-8")

        return 0


COMMANDS = LimitCPU
